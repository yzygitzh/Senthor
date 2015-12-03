from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from textblob import TextBlob
from django.core.context_processors import csrf

def search_post(request):
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