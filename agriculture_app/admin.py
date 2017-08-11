from django.contrib import admin
#from .models import Main_data
# Register your models here.

#第一种注册方法
# admin.site.register(Main_data)  #把 models 中的Article注册到后台管理（admin）中  localhost:8000/admin
'''
#第二种注册方法 显示其他字段
class Admin(admin.ModelAdmin):
    list_display = ('title','content','create_time')
    list_filter = ('create_time',)  #过滤器
admin.site.register(Main_data,Admin) #继承Admin
'''