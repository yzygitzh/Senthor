from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from textblob import TextBlob
from django.core.context_processors import csrf
from textblob.sentiments import NaiveBayesAnalyzer
def search_post_old(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    result="";
    ctx ={}
    ctx.update(csrf(request))
    ctx['rlt']="";
    if(request.POST):
        post_str=request.POST['q'];
        blob=TextBlob(post_str);
        for sentence in blob.sentences:
            tmp=sentence.sentiment.polarity;
            result='%f' %tmp;
            ctx['rlt']="sentiment polarity is "+result;
    

    return render(request,"post.html",ctx)
def search_post(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    NaivebayesResult="";
    ctx ={}
    ctx.update(csrf(request))
    ctx['naivebayes_rlt']="";
    ctx['PatternAnalyzer_rlt']="";
    if(request.POST):
        ctx['naivebayes_rlt']="naivebayes error";
        ctx['PatternAnalyzer_rlt']="PatternAnalyzer error";
        post_str=request.POST['q'];
        NaivebayesResult=getTextOverallSentiment(post_str);
        
        if(NaivebayesResult[0]=='pos'):
            sentiment='positive'
        else:
            sentiment='negtive'
        ctx['naivebayes_rlt']="NaiveBayes result:"+"classification="+sentiment+","+"p_pos="+str(NaivebayesResult[1])+","+"p_neg="+str(NaivebayesResult[2]);
        PatternAnalyzerResult=getPatternAnalyzerSentiment(post_str);
        ctx['PatternAnalyzer_rlt']="PatternAnalyzer result:"+"polarity:"+str(PatternAnalyzerResult['polarity'])+","+"subjectivity:"+str(PatternAnalyzerResult['subjectivity']);
    return render(request,"post.html",ctx)

def getTextOverallSentiment(text):
    blob=TextBlob(text,analyzer=NaiveBayesAnalyzer());
    result=();
    result=blob.sentiment;
    return result;
def getPatternAnalyzerSentiment(text):
    blob=TextBlob(text);
    result=();
    result=blob.sentiment;
    return result;
    
    