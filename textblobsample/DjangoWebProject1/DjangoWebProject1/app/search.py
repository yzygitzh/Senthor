from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from textblob import TextBlob
from django.core.context_processors import csrf

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
    result="";
    ctx ={}
    ctx.update(csrf(request))
    ctx['rlt']="";
    if(request.POST):
        post_str=request.POST['q'];
        result=getTextOverallSentiment(text);
        
        if(result[0]=='pos'):
            sentiment='positive'
        else:
            sentiment='negtive'
        ctx['rlt']="classification="+sentiment+"p_pos="+result[1]+"p_neg="+result[2];
    return render(request,"post.html",ctx)

def getTextOverallSentiment(text):
    blob=TextBlob(text);
    result=();
    result=blob.sentiment;
    return result;

    