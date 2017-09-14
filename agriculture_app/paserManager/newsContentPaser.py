# coding:utf-8
# 引入相关模块
import requests
from bs4 import BeautifulSoup
import re
import jieba
import requests
import sys
import urllib
# 设置爬取5类中的新闻个数
PASER_NUM = 50 # 爬的数量太多会影响网站使用效果
# 第一维是抓取的网址,第二维是标题key_select,第三维是新闻内容key_select
news_urls = {
    u"class_id1" : [ "http://www.farmer.com.cn/jjpd/zzy/zzdt/index_%d.htm"%(i) for i in range(1,13) ],
    u"class_id2": [ "http://www.gengzhongbang.com/2/index.php?page=%d"%(i) for i in range(1,20) ],
    u"class_id3": [ "http://www.guoshu123.cn/zz/list-909-%d.html"%(i) for i in range(2,20) ],
    u"class_id4": [
        "http://www.114guoshu.com/hangqing/shucai/",
        "http://www.114guoshu.com/hangqing/shuiguo/",
    ],
    u"class_id5": [ "http://www.206zz.com/baike/zcfg/" ],
}

def getSoup(url, code = "gb2312"):
    try:
        webdata = requests.get(url)
        webdata.encoding = code  # 根据网站的编码格式修改
        webdata = webdata.text
        # 对获取到的文本进行解析
        soup = BeautifulSoup(webdata,'html.parser')
        return soup
    except:
        return "error"

#获取新闻网址中的新闻内容
def getNewContent(url,select_key,code="gb2312"):
    if url[:5]!="http:":
        return []
    soup = getSoup(url,code)
    if soup=="error":
        return []
    content = soup.select(select_key)
    return content

# 爬取农业新闻网
def paserClass1():
    print ("paserClass1 ......")
    news_data = dict(); idx = 0 # 爬取内容数量
    for url in news_urls["class_id1"]:
        news_targets = getNewContent(url,"a.vvqqq")
        # 对返回的列表进行遍历
        for i,news_target in enumerate(news_targets,0):
            if idx >= PASER_NUM: return news_data
            title = news_target.get_text()
            content = getNewContent( url[:-11] + news_target.get("href")[2:], "div.content > div.TRS_Editor" )
            if len(content)==0:
                print("no content")
                continue
            print("has content ",idx)
            news_data[idx] = {
                "class_name": "农业新闻",
                "title": str(title.encode("utf-8")),
                "content": content[0].get_text(),
                "jieba_cut_content":" ".join( jieba.cut( str(content[0].get_text().encode("utf-8"))) ),
            }
            idx += 1
    return news_data

# 爬取病虫害网
def paserClass2():
    print ("paserClass2 ......")
    news_data = dict()
    idx = 0 # 爬取内容数量
    for url in news_urls["class_id2"]:
        news_targets = getNewContent(url,"dt.xs2 > a.xi2")
        # 对返回的列表进行遍历
        for i,news_target in enumerate(news_targets,0):
            if idx >= PASER_NUM: return news_data
            title = news_target.get_text()
            content = getNewContent( news_target.get("href"), "#article_content" )
            if len(content)==0:
                print("no content")
                continue
            print("has content ",idx)
            news_data[idx] = {
                "jieba_cut_content":" ".join( jieba.cut( str(content[0].get_text().encode("utf-8"))) ),
                "class_name": "病虫害",
                "title": str(title.encode("utf-8")),
                "content": content[0].get_text(),
            }
            idx += 1
    return news_data

# 爬取果蔬种植网 用时很久
def paserClass3():
    print("paserClass3 ......")
    news_data = dict()
    idx = 0 # 爬取内容数量
    for url in news_urls["class_id3"]:
        news_targets = getNewContent(url,"li.catlist_li a","utf-8")
        # 对返回的列表进行遍历
        for i,news_target in enumerate(news_targets,0):
            #print news_target
            if idx >= PASER_NUM: return news_data
            title = news_target.get_text()
            content = getNewContent( news_target.get("href"), "#article", code="utf-8")
            if len(content)==0:
                print("no content")
                continue
            print("has content ",idx)
            news_data[idx] = {
                "jieba_cut_content":" ".join( jieba.cut( str(content[0].get_text().encode("utf-8"))) ),
                "class_name": "果蔬种植",
                "title": str(title.encode("utf-8")),
                "content": content[0].get_text(),
            }
            idx += 1
    return news_data

# 农业信息网 该网址规则不同无法爬取
# 爬取价格新闻 该网址规则不同无法爬取
def paserClass4():
    print("paserClass4 ......")
    news_data = dict()
    idx = 0# 爬取内容数量
    for url in news_urls["class_id4"]:
        news_targets = getNewContent(url,"li.catlist_li a","utf-8")
        # 对返回的列表进行遍历
        for i,news_target in enumerate(news_targets,0):
            #print news_target
            if idx >= PASER_NUM: return news_data
            title = news_target.get_text()
            content = getNewContent( news_target.get("href"), "div.content", code="utf-8")
            if len(content)==0:
                print("no content")
                continue
            print("has content ",idx)
            news_data[idx] = {
                "jieba_cut_content":" ".join( jieba.cut( str(content[0].get_text().encode("utf-8"))) ),
                "class_name": "市场价格",
                "title": str(title.encode("utf-8")),
                "content": content[0].get_text(),
            }
            idx += 1
    return news_data

# 爬取果蔬种植网 用时很久
def paserClass5():
    print("paserClass5 ......")
    news_data = dict()
    idx = 0 # 爬取内容数量
    for url in news_urls["class_id5"]:
        news_targets = getNewContent(url,"a.title","utf-8")
        # 对返回的列表进行遍历
        for i,news_target in enumerate(news_targets,0):
            #print news_target
            if idx >= PASER_NUM: return news_data
            title = news_target.get_text()
            content = getNewContent( "http://www.206zz.com"+news_target.get("href"), "div.showofcontent_jiankang", code="utf-8")
            if len(content)==0:
                print("no content")
                continue
            print("has content ",idx)
            news_data[idx] = {
                "jieba_cut_content":" ".join( jieba.cut( str(content[0].get_text().encode("utf-8"))) ),
                "class_name": "政策法规",
                "title": str(title.encode("utf-8")),
                "content": content[0].get_text(),
            }
            idx += 1
    return news_data

def paserWeather():
    print("paserWeather ......")
    urls = [
        "http://www.weather.com.cn/weather/101270101.shtml", #未来七天气象
    ]
    weather_data = []
    idx = 0 # 爬取内容数量
    for url in urls:
        weather_targets = getNewContent(url,"div.c7d ul li","utf-8")
        # 对返回的列表进行遍历
        for i,weather_target in enumerate(weather_targets,0):
            #print weather_target
            content = weather_target.get_text()
            print("has content ",idx)
            weather_data.append( content )
            idx += 1
    return weather_data

if __name__ == '__main__':
    news_dict = paserWeather()
    print(news_dict[0])
