# -*- coding: utf-8 -*-
#encoding:utf=8
import pymongo as pm
import json

class MongoOperator:
    def __init__(self, host, port, db_name, default_collection):
        '''
        设置mongodb的地址，端口以及默认访问的集合，后续访问中如果不指定collection，则访问这个默认的
        :param host: 地址
        :param port: 端口
        :param db_name: 数据库名字
        :param default_collection: 默认的集合
        '''
        #建立数据库连接
        self.client = pm.MongoClient(host=host, port=port)
        #选择相应的数据库名称
        self.db = self.client.get_database(db_name)
        #设置默认的集合
        self.collection = self.db.get_collection(default_collection)

    def insert(self, item, collection_name =None):
        '''
        插入数据，这里的数据可以是一个，也可以是多个
        :param item: 需要插入的数据
        :param collection_name:  可选，需要访问哪个集合
        :return:
        '''
        if collection_name != None:
            collection = self.db.get_collection(collection_name)
            collection.insert(item)
        else:
            self.collection.insert(item)

    def find(self, expression =None, collection_name=None):
        '''
        进行简单查询，可以指定条件和集合
        :param expression: 查询条件，可以为空
        :param collection_name: 集合名称
        :return: 所有结果
        '''
        if collection_name != None:
            collection = self.db.get_collection(collection_name)
            if expression == None:
                return collection.find()
            else:
                return collection.find(expression)
        else:
            if expression == None:
                return self.collection.find()
            else:
                return self.collection.find(expression)

    # 删除该数据库中的集合
    def remove(self,collection_name=None):
        if collection_name is None: return
        self.db.get_collection(collection_name).drop()

    def update(self, update_key1, update_key2,collection_name=None ):
        if collection_name != None:
            collection = self.db.get_collection(collection_name)
        else:
            collection = self.collection
        return collection.update(update_key1,update_key2,upsert=True)

if __name__ == '__main__':
    db = MongoOperator('localhost',27017,'Data','test_collection1')
    print (db.db.users)
    item = {}
    item['name'] = 'pengzheng'
    item['age'] = '10'
    db.insert(item,"test_collection1")
    for item in db.find(collection_name="test_collection1"):
        print(item)
    db.remove("test_collection1")


