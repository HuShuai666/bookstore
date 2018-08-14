from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from apps.Comment.models import Comments
from apps.art_apps.models import Arts


def art(request):
    if request.method=='GET':
        arts=Arts.objects.all()
        return render(request,'artsuser/content.html',{'arts':arts})
    elif request.method=='POST':
        ac_id=request.POST.get('ac_id')
        name=request.POST.get('name')
        title=request.POST.get('title')
        content=request.POST.get('content')
        Comments.objects.create(name=name,title=title,content=content,arts_id=ac_id)
        return render(request,'detail/success.html')


