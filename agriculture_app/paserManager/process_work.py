from http import cookiejar
from multiprocessing import Pool
from urllib import request

from agriculture_app.models import price
from agriculture_app.paserManager import price

from selenium import webdriver
import time
import re

def getCookie_value(url):
    driver = webdriver.Chrome()
    # driver.maximize_window()  #屏幕最大化
    driver.get(url)
    source = driver.page_source
    pattern = re.compile(r'<body value="(.*?)">', re.S)
    value = re.findall(pattern, source)[0].strip()

    # get the session cookie
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    # print cookie
    cookiestr = ';'.join(item for item in cookie)
    li = [value + '\n', cookiestr + '\n']
    with open(r'F:\my_projects\python\Agriculture\agriculture_app\io\cookie.txt', 'w', encoding='utf-8') as f:
        f.writelines(li)

    time.sleep(5)
    driver.quit()
def getCookie():
    list = []
    with open(r'F:\my_projects\python\Agriculture\agriculture_app\io\cookie.txt', 'r', encoding='utf-8') as f:
        for item in f.readlines():
            list.append(item.strip())
    return list

if __name__ == '__main__':
    '''
    for i in range(10):
        main(i*10)
    '''
    cookie_url = 'http://www.3w3n.com/user/price4Day/goIndex'
    cookie_value = getCookie_value(cookie_url)
    pool = Pool(processes=4)  # 建立进程池
    pool.map(price.main, (typeId for typeId in range(1,2001)))  # 映射到主函数中进行循环
    print('["价格"]数据采集完毕..........')
