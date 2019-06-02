import urllib.request
import os

def open_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400')
    return urllib.request.urlopen(req).read()

def find_pic(url):
    html = open_url(url).decode('utf-8')
    pic_addrs = []
    a = html.find('src="http')
    while a != -1:
        b = html.find('.jpg"', a, a + 255)
        if  b != -1:
            pic_addrs.append(html[a + 5 : b + 4])
        else:
            b = a + 5
        a = html.find('src="http', b)
    return pic_addrs

def save_pic(pic_addrs):
    for each in pic_addrs:
        with open(each.split('/')[-1], 'wb') as file:
            file.write(open_url(each))

def picture(start = 1, end = 1, url = 'https://tieba.baidu.com', folder = '1'):
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    if url.find('?pn=') != -1:
        url = url[:url.find('?pn=')]
    for i in range(int(start), int(end) + 1):
        url = url + '?pn=' + str(i)
        pic_addrs = find_pic(url)
        save_pic(pic_addrs)

print("爬取图片")
url = input("网址(贴吧某贴):")
start = input("起始页:")
end = input("结束页:")
folder = input("存放地址:")
picture(start, end, url, folder)