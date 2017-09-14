from agriculture_app.models import *
from agriculture_app.tools.random_num import *
import base64

def home_function(request):
    articles = page.objects.all()
    return render(request, 'home_.html', {'articles': articles})


def article(request, page_id):
    articles = main_data.objects.get(myId=str(page_id))  # 和url中的 page_id  名字一样
    return render(request, 'article.html', {'articles': articles})


def edit_page(request, page_id):
    if str(page_id) == '0':  # 数据库中id 从1开始的
        return render(request, 'edit_page.html')
    articles = main_data.objects.get(myId=str(page_id))
    return render(request, 'edit_page.html', {'articles': articles})


def edit_action(request):
    title = request.POST.get('title', 'TITLE')
    content = request.POST.get('content', 'CONTENT')
    article_id = request.POST.get('article_id', '0')
    if article_id == '0':
        is_have = True
        while is_have == True:
            myId1 = random_num()
            # 和数据库中的数据对比
            user = main_data.objects.filter(myId=myId1)
            if user:
                #return HttpResponse('已经存在')
                is_have = True
            else:
                main_data.objects.create(myId=myId1, title=title, content=content)  # 存到数据库
                is_have = False
        # 返回到主页
        articles = main_data.objects.all()
        return render(request, 'home_.html', {'articles': articles})
    else:
        articles = main_data.objects.get(myId=str(article_id))
        articles.title = title
        articles.content = content
        articles.save()
        return render(request, 'article.html', {'articles': articles})


# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

    def register(request):
        if request.method == 'POST':
            userform = UserForm(request.POST)
            if userform.is_valid():
                username = userform.cleaned_data['username']
                password = userform.cleaned_data['password']
                email = userform.cleaned_data['email']

                # 和数据库中的数据对比
                user = User.objects.filter(username__exact=username)
                if user:
                    return HttpResponse('用户已经存在')
                else:
                    User.objects.create(username=username, password=password, email=email)
                    articles = main_data.objects.all()
                    return render(request, 'home_.html', {'articles': articles})

                # User.save()
        else:
            userform = UserForm()
        return render_to_response('register.html', {'userform': userform})

    def login(request):
        if request.method == 'POST':
            userform = UserForm(request.POST)
            if userform.is_valid():
                username = userform.cleaned_data['username']
                password = userform.cleaned_data['password']

                # 和数据库中的数据对比
                user = User.objects.filter(username__exact=username, password__exact=password)

                if user:
                    articles = main_data.objects.all()
                    return render(request, 'home_.html', {'articles': articles})
                    # return render_to_response('home.html',{'userform':userform})
                else:
                    return HttpResponse('用户名或密码错误,请重新登录')

        else:
            userform = UserForm()
        return render_to_response('login.html', {'userform': userform})


def newsHandle(request,page_id):
    articles = page.objects.get(pageId = str(page_id))
    # for key in articles.content:
    #     print(articles.content[key])
    return render(request, 'test.html', {'articles': articles})
