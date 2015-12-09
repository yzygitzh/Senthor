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
def survey_post(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    ctx ={}
    ctx.update(csrf(request))
    ctx['survey_result']="";
    if(request.POST):
        entry={};#字典需要声明
        entry['name']=request.POST['name'];
        entry['age']=request.POST['age'];
        entry['gender']=request.POST['gender'];
        entry['email']=request.POST['email'];
        insert(entry);
        result=getAll();
        retList=[];
        for var in result:
            #ctx['survey_result']+='<li>'+'<input type="checkbox" name="todel[]" value="'+str(var.id)+'"/>'+str(var.name)+','+str(var.age)+','+str(var.gender)+','+str(var.email)+'</li>';
            retList.append(var);
        ctx['survey_result']=retList;
    return render(request,"survey.html",ctx)

from app.models import PersonInfo
def insert(entry):
    db=PersonInfo()
    db.age=entry['age'];
    db.email=entry['email'];
    db.name=entry['name']
    db.gender=entry['gender'];
    db.save();
def getAll():
    list=PersonInfo.objects.all();
    return list;
def delete(del_id):
    del_obj=PersonInfo.objects.get(id=del_id);
    del_obj.delete();
def survey_del(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    ctx ={}
    ctx.update(csrf(request))
    ctx['survey_result']="";
    if(request.POST):
        entry=request.POST.getlist(key='todel[]');
        for var in entry:
            delete(int(var));
        result=getAll();
        retList=[];
        for var in result:
            #ctx['survey_result']+='<li>'+'<input type="checkbox" name="todel[]" value="'+str(var.id)+'"/>'+str(var.name)+','+str(var.age)+','+str(var.gender)+','+str(var.email)+'</li>';
            retList.append(var);
        ctx['survey_result']=retList;
    return render(request,"survey.html",ctx)
def survey_show(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    ctx ={}
    ctx.update(csrf(request))
    ctx['survey_result']="";

    result=getAll();
    retList=[];
    for var in result:
        #ctx['survey_result']+='<li>'+'<input type="checkbox" name="todel[]" value="'+str(var.id)+'"/>'+str(var.name)+','+str(var.age)+','+str(var.gender)+','+str(var.email)+'</li>';
        retList.append(var);
    ctx['survey_result']=retList;
    return render(request,"survey.html",ctx)