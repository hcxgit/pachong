#coding = utf-8
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
GROUP_START = 1   # offset
GROUP_END = 20
#请求页面，返回值为json
#更新一下
def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count':  '20',
        'cur_tab':  '1',
        'from': 'search_tab'
    }
    r_url = 'https://www.toutiao.com/search_content/?'
    URL = r_url + urlencode(params)
    try:
        request_page = requests.get(URL)
        if request_page.status_code == 200:
            return request_page.json()
    except requests.ConnectionError:
        return None
#解析   返回图片的字典
def get_imgs(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if images:
                for image in images:
                    yield {
                        'image':image.get('url'),
                        'title':title
                    }
#保存图片
def save_image(image_dic):
    if not os.path.exists(image_dic.get('title')):  #os.path.exists()  检测某个文件或者目录是否存在
        i =image_dic.get('title').replace('\n','')
        os.mkdir(i)
    try:
        response = requests.get('http:'+image_dic.get('image'))
        if response.status_code == 200:
            file_path ='{0}/{1}.{2}'.format(image_dic.get('title'),md5(response.content).hexdigest(),'jpg')  # md5.hexdigest()通过哈希函数对每个文件进行文件名的自动生成
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:  #  rb、wb  可以对二进制数据如图像声音等进行读写
                    f.write(response.content)
            else:
                print('已经下载了',file_path)
    except requests.ConnectionError:
        print('保存失败')
#构造offset数组遍历，提取图片链接下载
def main(offset):
    json = get_page(offset)
    for image_dic in get_imgs(json):
        print(image_dic)
        save_image(image_dic)

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START,GROUP_END+1)])
    # for group in groups:
    #     main(group)
    pool.map(main, groups)
    pool.close()
    pool.join()
