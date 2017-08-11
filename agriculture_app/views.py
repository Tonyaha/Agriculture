from django.db import models
from django.shortcuts import render

# Create your views here.
from agriculture_app.models import main_data


def home_function(request):
    articles = main_data.objects.all()
    return render(request,'home_.html',{'articles':articles})

def article(request,page_id):
    articles = main_data.objects.get(myId=str(page_id))  #和url中的 page_id  名字一样
    return render(request, 'article.html', {'articles': articles})

def edit_page(request,page_id):
    if str(page_id) == '0': #数据库中id 从1开始的
        return render(request, 'edit_page.html')
    articles = main_data.objects.get(myId=str(page_id))
    return render(request, 'edit_page.html', {'articles': articles})
def edit_action(request):
    title = request.POST.get('title','TITLE')
    content = request.POST.get('content','CONTENT')
    article_id = request.POST.get('article_id','0')
    if article_id == '0':
        main_data.objects.create(myId=5,title=title, content=content)  # 存到数据库
        # 返回到主页
        articles = main_data.objects.all()
        return render(request, 'home_.html', {'articles': articles})
    else:
        articles = main_data.objects.get(myId=str(article_id))
        articles.title = title
        articles.content = content
        articles.save()
        return render(request, 'article.html', {'articles': articles})

def myId():

    return 5


def register(request):
    return render(request,'register.html')
def register_response(request):
    title = request.POST.get('title','TITLE')
    content = request.POST.get('content','CONTENT')
    main_data.objects.create(title=title, content=content)  #存到数据库

    #返回到主页
    articles = main_data.objects.all()
    return render(request, 'home_.html', {'articles': articles})

def login(request):
    articles = main_data.objects.all()
    return render(request, 'login.html',{'articles':articles})
def login_response(request):

    # 返回到主页
    articles = main_data.objects.all()
    return render(request, 'home_.html', {'articles': articles})