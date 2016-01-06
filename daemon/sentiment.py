import ...
class Sentiment(lazydict):
    def __init__(self, path="", language=None, synset=None, confidence=None, **kwargs):
        self._path       = path
        self._language   = None
        self._confidence = None
        self._synset     = synset
        self._synsets    = {}
        self.labeler     = {}
        self.tokenizer   = kwargs.get("tokenizer", find_tokens)
        self.negations   = kwargs.get("negations", ("no", "not", "n't", "never"))
        self.modifiers   = kwargs.get("modifiers", ("RB",))
        self.modifier    = kwargs.get("modifier" , lambda w: w.endswith("ly"))

    def load(self, path=None):
        if not path:
            path = self._path
        if not os.path.exists(path):
            return
        words, synsets, labels = {}, {}, {}
        xml = cElementTree.parse(path)
        xml = xml.getroot()
        for w in xml.findall("word"):
            if self._confidence is None \
            or self._confidence <= float(w.attrib.get("confidence", 0.0)):
                w, pos, p, s, i, label, synset = (
                    w.attrib.get("form"),
                    w.attrib.get("pos"),
                    w.attrib.get("polarity", 0.0),
                    w.attrib.get("subjectivity", 0.0),
                    w.attrib.get("intensity", 1.0),
                    w.attrib.get("label"),
                    w.attrib.get(self._synset)
                )
                psi = (float(p), float(s), float(i))
                if w:
                    words.setdefault(w, {}).setdefault(pos, []).append(psi)
                if w and label:
                    labels[w] = label
                if synset:
                    synsets.setdefault(synset, []).append(psi)
        self._language = xml.attrib.get("language", self._language)
        for w in words:
            words[w] = dict((pos, [avg(each) for each in zip(*psi)]) for pos, psi in words[w].items())
        for w, pos in list(words.items()):
            words[w][None] = [avg(each) for each in zip(*pos.values())]
        for id, psi in synsets.items():
            synsets[id] = [avg(each) for each in zip(*psi)]
        dict.update(self, words)
        dict.update(self.labeler, labels)
        dict.update(self._synsets, synsets)

    def __call__(self, s, negation=True, **kwargs):
        def avg(assessments, weighted=lambda w: 1):
            s, n = 0, 0
            for words, score in assessments:
                w = weighted(words)
                s += w * score
                n += w
            return s / float(n or 1)
        if hasattr(s, "gloss"):
            a = [(s.synonyms[0],) + self.synset(s.id, pos=s.pos) + (None,)]
        elif isinstance(s, basestring) and RE_SYNSET.match(s):
            a = [(s.synonyms[0],) + self.synset(s.id, pos=s.pos) + (None,)]
        elif isinstance(s, basestring):
            a = self.assessments(((w.lower(), None) for w in " ".join(self.tokenizer(s)).split()), negation)
        elif hasattr(s, "sentences"):
            a = self.assessments(((w.lemma or w.string.lower(), w.pos[:2]) for w in chain(*s)), negation)
        elif hasattr(s, "lemmata"):
            a = self.assessments(((w.lemma or w.string.lower(), w.pos[:2]) for w in s.words), negation)
        elif hasattr(s, "lemma"):
            a = self.assessments(((s.lemma or s.string.lower(), s.pos[:2]),), negation)
        elif hasattr(s, "terms"):
            a = self.assessments(chain(*(((w, None), (None, None)) for w in s)), negation)
            kwargs.setdefault("weight", lambda w: s.terms[w[0]])
        elif isinstance(s, dict):
            a = self.assessments(chain(*(((w, None), (None, None)) for w in s)), negation)
            kwargs.setdefault("weight", lambda w: s[w[0]])
        elif isinstance(s, list):
            a = self.assessments(((w, None) for w in s), negation)
        else:
            a = []
        weight = kwargs.get("weight", lambda w: 1)
        return Score(polarity = avg( [(w, p) for w, p, s, x in a], weight ),
                 subjectivity = avg([(w, s) for w, p, s, x in a], weight),
                  assessments = a)

    def assessments(self, words=[], negation=True):
        a = []
        m = None
        n = None
        for w, pos in words:
            if w is None:
                continue
            if w in self and pos in self[w]:
                p, s, i = self[w][pos]
                if m is None:
                    a.append(dict(w=[w], p=p, s=s, i=i, n=1, x=self.labeler.get(w)))
                if m is not None:
                    a[-1]["w"].append(w)
                    a[-1]["p"] = max(-1.0, min(p * a[-1]["i"], +1.0))
                    a[-1]["s"] = max(-1.0, min(s * a[-1]["i"], +1.0))
                    a[-1]["i"] = i
                    a[-1]["x"] = self.labeler.get(w)
                if n is not None:
                    a[-1]["w"].insert(0, n)
                    a[-1]["i"] = 1.0 / a[-1]["i"]
                    a[-1]["n"] = -1
                m = None
                n = None
                if pos and pos in self.modifiers or any(map(self[w].__contains__, self.modifiers)):
                    m = (w, pos)
                if negation and w in self.negations:
                    n = w
            else:
                if negation and w in self.negations:
                    n = w
                elif n and len(w.strip("'")) > 1:
                    n = None
                if n is not None and m is not None and (pos in self.modifiers or self.modifier(m[0])):
                    a[-1]["w"].append(n)
                    a[-1]["n"] = -1
                    n = None
                elif m and len(w) > 2:
                    m = None
                if w == "!" and len(a) > 0:
                    a[-1]["w"].append("!")
                    a[-1]["p"] = max(-1.0, min(a[-1]["p"] * 1.25, +1.0))
                if w == "(!)":
                    a.append(dict(w=[w], p=0.0, s=1.0, i=1.0, n=1, x=IRONY))
                if w.isalpha() is False and len(w) <= 5 and w not in PUNCTUATION:
                    for (type, p), e in EMOTICONS.items():
                        if w in imap(lambda e: e.lower(), e):
                            a.append(dict(w=[w], p=p, s=1.0, i=1.0, n=1, x=MOOD))
                            break
        for i in range(len(a)):
            w = a[i]["w"]
            p = a[i]["p"]
            s = a[i]["s"]
            n = a[i]["n"]
            x = a[i]["x"]
            a[i] = (w, p * -0.5 if n < 0 else p, s, x)
        return a
