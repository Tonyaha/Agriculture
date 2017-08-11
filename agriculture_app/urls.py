from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^home/$', views.home_function),
    url(r'^article/(?P<page_id>[0-9]+)$', views.article, name='article_page'),
    #url(r'^article/(?P<page_id>[0-9]+)$', views.article, name='article_page'),

    #url(r'^edit/(?P<page_id>[0-9]+)$', views.edit_page,name='edit_page'),
    url(r'^edit/(?P<page_id>[0-9]+)$', views.edit_page,name='edit_page'),
    url(r'^edit/action$', views.edit_action,name='edit_action'),

    url(r'^register/$', views.register,name='register_page'),
    url(r'^register/response$', views.register_response, name='register_response'),

    url(r'^login/$', views.login, name='login_page'),
]