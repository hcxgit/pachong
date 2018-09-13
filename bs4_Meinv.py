#coding = utf-8
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
import lxml
from multiprocessing.pool import Pool
#####   代理：proxies = {"https": "https://183.129.207.73:14823", "https": "https://114.215.95.188:3128", }
#请求页面，返回值为json
def get_page(n):
    URL = 'http://www.27270.com/tag/134_' + str(n)+'.html'
    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    try:
        html = requests.get(URL,headers=heads)
        if html.status_code == 200:
            return html
    except requests.ConnectionError:
        return None

#解析   返回图片的字典
def get_imgs(html):
    soup = BeautifulSoup(html, 'lxml')
    for ul in soup.find_all(class_="w110 oh Tag_list"):
        for li in ul.find_all(name='li'):
            if li:
                yield {
                    'image': li.img['src'],
                    'title': li.img['alt']
                }
#保存图片
def save_image(image_dic):
    if not os.path.exists('美女图片'):  #os.path.exists()  检测某个文件或者目录是否存在
        os.mkdir('美女图片')
    try:
        response = requests.get(image_dic.get('image'))
        if response.status_code == 200:
            file_path ='{0}/{1}.{2}'.format('美女图片',md5(response.content).hexdigest(),'jpg')  # md5.hexdigest()通过哈希函数对每个文件进行文件名的自动生成
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:  #  rb、wb  可以对二进制数据如图像声音等进行读写
                    f.write(response.content)
            else:
                print('已经下载了',file_path)
    except requests.ConnectionError:
        print('保存失败')
    except requests.HTTPError as f:
        print('The server couldn\'t fulfill the request.')

#提取图片链接下载
def main(n):
    if get_page(n):
        html = get_page(n).text
        print(html)
        if get_imgs(html):
            for image_dic in get_imgs(html):
                print(image_dic)
                save_image(image_dic)

if __name__ == '__main__':
    pool = Pool()
    groups = ([x  for x in range(11,13)])
    pool.map(main, groups)
    pool.close()
    pool.join()

