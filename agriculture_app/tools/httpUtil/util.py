from urllib import error,request
from  lxml import etree  #整理html
from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from PIL import Image,ImageFile
from io import BytesIO
import requests

# 数据获取（不整理html）
class HttpUtil():
    def __init__(self,url,headers,code):
        self.url = url
        self.headers = headers
        self.code = code

    def getHtml(self,url):
        try:
            response = requests.get(url,headers=self.headers)
            response.encoding = self.code
            html = response.text
            #req = request.Request(url=url, headers=self.headers)
            # response = request.urlopen(req)
            # html = response.read().decode(self.code, 'ignore')
            # #result = etree.parse(html)
            # #etree.tostring(result,pretty_print=True)
            # response.close()  #urlopen() 关闭response,防止远程主机 关闭连接
        except error.HTTPError as e:
            print(e.code)
        except error.URLError as e:
            print(e.reason)
        return html

    def webDriver(self):
        #  不整理..........
        driver = webdriver.Chrome()
        driver.get(self.url)
        source = driver.page_source
        # get the session cookie
        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
        # print cookie
        cookiestr = ';'.join(item for item in cookie)
        time.sleep(5)
        driver.quit()  #关闭浏览器
        return cookiestr + '\n' + source

    def getData(self,html,key,flag):
        if flag==1:
            result = re.findall(key,html)
        if flag==2:
            soup = BeautifulSoup(html,'lxml')
            result = soup.find_all(key)
        return result

    def saveImg(self, imageURL,fileName):
        # array = np.asarray(image)  # 将image 转换成numpy数组
        # print(image.format, image.size, image.mode)
        # image.show()
        # ImageFile.LOAD_TRUNCATED_IMAGES = True  # OSError: image file is truncated
        # response = requests.get(imageURL, headers=self.headers)
        # image = Image.open(BytesIO(response.content))
        # image.save(imagePath)
        img = requests.get(imageURL, headers=self.headers)
        imagePath = r'F:\my_projects\python\Agriculture\agriculture_app\static\image\\'+fileName
        try:
            f = open(imagePath, 'ab')  # 解决不能识别图像文件 ？？
            f.write(img.content)
            f.close()
        except:
            return None
        path = 'image\\'+fileName
        return path




