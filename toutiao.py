from urllib.parse import urlencode
import requests,time,os
from hashlib import md5
from multiprocessing.pool import Pool

def get_page(offset):
    parms = {
        'aid':'24',
        'app_name':'web_search',
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'en_qc':'1',
        'cur_tab':'1',
        'from':'search_tab',
        'pd':'synthesis',
        'timestamp':str(int(round(time.time()*1000)))
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(parms)
    try:
        response =requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('title') is None:
                continue
            else:
                title = item.get('title')
                images = item.get('image_list')
                for image in images:
                    yield {
                        'image':image.get('url'),
                        'title':title
                    }

def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')#使用md5加密
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)

GROUP_START = 0
GROUP_END = 4

if __name__ == '__main__':
    pool = Pool()
    groups = ([x*20 for x in range(GROUP_START,GROUP_END+1)])
    pool.map(main,groups)
    pool.close()
    pool.join()
