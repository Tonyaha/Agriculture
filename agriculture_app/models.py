
# Create your models here. 一个model对应数据库一张数据表
from django.db import models
from mongoengine import *
from datetime import datetime

# 连接数据库
connect('Data')  # 连接本地blog数据库
#connect('Data',host='127.0.0.1',port='27017')

# 如需验证和指定主机名
# connect('blog', host='192.168.3.1', username='root', password='1234')

class user(Document):
    userId = IntField(required=True)
    # id = ObjectIdField(primary_key=True,required=True)
    user = StringField(max_length=1000, required=True)
    password = StringField(max_length=1000, required=True)


class main_data(Document):

    ' 继承Document类,为普通文档 '
    myId = IntField( required=True)
    #id = ObjectIdField(primary_key=True,required=True)
    title = StringField(max_length=1000, required=True)
    content = StringField(max_length=1000, required=True)



'''
class Main_data(models.Model):
    title = models.CharField(max_length=32,default='Title')
    content = models.TextField(null=True)
    create_time = models.DateTimeField(null=True) #创建对象的时添加当前时间

    def __str__(self):  #解决后台（admin）管理中只显示 Article object 这样一个对象
        return self.title

'''