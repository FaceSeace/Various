from bs4 import BeautifulSoup
from multiprocessing import Pool
import requests, time, re, os

def get_imgs(url, all_img='0'):
    if all_img == '1':
        from selenium import webdriver
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(5)
        try:
            driver.get(url)
        except:
            pass
        for i in range(9):
            print(i + 1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        #html = driver.execute_script("return document.documentElement.outerHTML")
        html = driver.page_source
        driver.quit()
    else:
        html = requests.get(url).text
    img_master_list = re.findall(r'data-src="(https://i\.pximg\.net/.*?_master1200\.jpg)"', str(BeautifulSoup(html, 'lxml').find_all(class_='_layout-thumbnail')))
    print("总张数:" + str(len(img_master_list)))
    img_original_list = []
    for img in img_master_list:
        img = img.replace(re.search("c/.*?/img-master", img).group(), "img-original")
        img = img.replace("_master1200.jpg", ".png")
        img_original_list.append(img)
    return img_original_list

def download_img(url):
    id = re.search(r'/(\d*?)_', url).group(1)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    header['Referer'] = 'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + id
    img = requests.get(url, headers=header).content
    if len(img) < 100:
        url = url.replace(".png", ".jpg")
        img = requests.get(url, headers=header).content
    with open(url.rsplit('/', 1)[-1], 'wb') as file:
        file.write(img)
        print(file.name)

if __name__ == "__main__":
    file = input("存放文件夹名:")
    name = input("插画类型(今日-0 本周-1 本月-2 新人-3):")
    if name == "今日" or name == '0':
        type_name = "daily"
    elif name == "本周" or name == '1':
        type_name = "weekly"
    elif name == "本月" or name == '2':
        type_name = "monthly"
    elif name == "新人" or name == '3':
        type_name = "rookie"
    else:
        print("类型错误")
        time.sleep(1)
        exit()
    year = input("年:")
    month = input("月:")
    day = input("日:")
    process = input("启动进程数:")
    all_img = input("是否下载所有图片(是-1 否-0):")
    if all_img == "是":
        all_img = '1'
    if int(process) < 1:
        print("进程太少")
        time.sleep(1)
        exit()
    if not os.path.exists(file):
        os.mkdir(file)
    os.chdir(file)
    url = "https://www.pixiv.net/ranking.php?mode={}&content=illust&date={}{}{}".format(type_name, year, month.zfill(2), day.zfill(2))
    urls = get_imgs(url, all_img)
    pool = Pool(int(process))
    for url in urls:
        pool.apply_async(download_img, (url, ))
    pool.close()
    pool.join()
