import urllib.request
import urllib.parse
import json

while True:
    content = input("请输入需要翻译的内容:")

    url = 'http://fanyi.youdao.com/translate'
    head = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400'}
    data = {'i' : content,
            'from' : 'AUTO',
            'to' : 'AUTO',
            'smartresult' : 'dict',
            'client' : 'fanyideskweb',
            'salt' : '1536596147300',
            'sign' : '7db375c57448209e133561324f175e8c',
            'doctype' : 'json',
            'version' : '2.1',
            'keyfrom' : 'fanyi.web',
            'action' : 'FY_BY_REALTIME',
            'typoResult' : 'false'}
    data = urllib.parse.urlencode(data).encode("utf-8")
    response = urllib.request.Request(url,data,head)
    result = json.loads(urllib.request.urlopen(response).read().decode("utf-8"))

    print("翻译结果:%s" % (result['translateResult'][0][0]['tgt']))