from http import cookiejar
from urllib import request
from urllib import error
import re
import time
from agriculture_app.models import price
# import chardet #自动获取网页编码方式  pip install chardet

# def getOpener(head):
#     cookie = cookiejar.CookieJar()
#     pro = request.HTTPCookieProcessor(cookie)
#     opener = request.build_opener(pro)
#     header = []
#     for key, value in head.items():
#         elem = (key, value)
#         header.append(elem)
#     opener.addheaders = header
#     return opener
#cookie = 'JSESSIONID=778704566E86136EE5E3F77A3F68C13A'


head = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Proxy-Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235',
    'Referer': 'http://www.3w3n.com/user/price4Day/goIndex',
    #'Cookie': cookie,
    'Host': 'www.3w3n.com',
}

# def getCookie(cookie_url):
#     session = requests.session()
#     response = session.get(url=cookie_url, headers=head)
#     cookie = ('; '.join(['='.join(item) for item in response.cookies.items()]))
#     print(cookie)
#     # for item in cookie:
#     #     print('Name = %s' % item.name)
#     #     print('Value = %s' % item.value)
#     return cookie


def getHtml(url):
    filename = 'cookie.txt'
    # 创建MozillaCookieJar实例对象
    cookie = cookiejar.MozillaCookieJar(filename)
    # 从文件中读取cookie内容到变量
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    pattern = re.compile(r'<div style="width:100%;height:100px;line-height: 100px;text-align: center;">暂无数据</div>',re.S)
    req = request.Request(url, headers=head)
    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.'+str(cookie))
    try:
        # print(url)
        req.add_header('Cookie', str('JSESSIONID=D45756F0A496C1D64D4D735622E7D2C3'))
        response = opener.open(req)#request.urlopen(req)  #
        html = response.read().decode('utf-8', 'ignore')
        result = re.findall(pattern, html)
        if result:
            print('暂没数据')
            time.sleep(10)
        else:
            getData(html)
            time.sleep(10)
    except error.HTTPError as e:
        print(e.code)
    except error.URLError as e:
        print(e.reason)


def getData(html):
    pattern = re.compile(r'<tr>.*?</tr>', re.S)
    pattern_item = re.compile(r'<div.*?>(.*?)</div>', re.S)
    pattern_add = re.compile(r'<a title="查看详情".*?>(.*?)</a>', re.S)
    tr = re.findall(pattern, html)
    for td in tr[1:]:
        isHave = re.findall(pattern_item, td)
        # print(isHave)
        if isHave != None:
            name = isHave[0].strip()
            average = isHave[1].strip().replace('&nbsp', '').replace(';', '')
            market = re.findall(pattern_add, isHave[2])[0]
            date_create = isHave[4].strip()
            # 和数据库中的数据对比
            all_data = price.objects.filter(name=name, market=market, average=average, date=date_create)
            # print(type(all_data))
            data = price.objects.filter(name=name, market=market)
            if all_data:
                print('>>>>数据已经存在<<<<')
                continue
            else:
                if data:
                    one_item = price.objects.get(name=name, market=market)
                    date = one_item.date
                    pro_average = one_item.average
                    week_price = one_item.week_price
                    # print(date,average)

                    now_time = int(time.time())  # 当前时间的时间戳

                    # 数据库里面的时间
                    timeArray = time.strptime(date, "%Y-%m-%d")
                    pro_time = int(time.mktime(timeArray))

                    # 当前数据的时间戳
                    timeArray1 = time.strptime(date_create, "%Y-%m-%d")
                    data_time = int(time.mktime(timeArray1))

                    if (now_time - pro_time) >= (now_time - data_time):
                        print('.....数据更新中')
                        price.objects.filter(name=name, market=market).update(average=average, date=date_create)
                    else:
                        print('时间超前了......')
                        continue
                        # continue

                    six_date = 432000
                    week_before = 1209600  # 14天内  #604800 八天内

                    if six_date <= (now_time - pro_time) < week_before:
                        # if week_price != None:
                        #     price.objects.filter(name=name, market=market).update(week_price=pro_average)
                        # else:
                        price.objects.filter(name=name, market=market).update(week_price=pro_average, date=date_create)
                        print('更新一周之前的价格中.........')
                    elif (now_time - pro_time) >= week_before:
                        price.objects.filter(name=name, market=market).update(week_price='上一次更新数据太久远')
                else:
                    print('正在保存数据.......')
                    cate = price(name=name, market=market, average=average, date=date_create)
                    cate.save()
                    # price1.objects.create(list)  # 存到数据库
                    # print(name+' '+average+' '+market+' '+date)
        else:
            print('暂时没数据')


def main(typeId):
    url = 'http://www.3w3n.com/user/price4Day/showPriceListPage?&typeId=' + str(typeId) + '&province=%E5%9B%9B%E5%B7%9D%E7%9C%81&r=9194EBB90AA1299848DEA8BC6F4996B7'
    html = getHtml(url)

#
# if __name__ == '__main__':
#     '''
#     for i in range(10):
#         main(i*10)
#     '''
#     pool = Pool(processes=10)  # 建立进程池
#     pool.map(main, (i for i in range(1, 2002)))  # 映射到主函数中进行循环
#     print('数据采集完毕..........')
