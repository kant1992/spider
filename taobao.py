from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
from pyquery import PyQuery as pq
from selenium.webdriver import ChromeOptions
import time,json

'''chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
brower = webdriver.Chrome(chrome_options=chrome_options)'''#无界面
brower = webdriver.Chrome()
wait = WebDriverWait(brower,10)
KEYWORD = 'iPad'

def index_page(page):
    print('正在爬取第',page,'页')
    try:
        brower.get('https://s.taobao.com')
        time.sleep(30)
        brower.refresh()
        cookies = brower.get_cookies()
        jsoncookies = json.dumps(cookies)
        with open('cookies','w') as  f:
            f.write(jsoncookies)
        brower.close()
        brower.get('https://s.taobao.com')
        time.sleep(10)
        brower.delete_all_cookies()
        with open('cookies','r',encoding='utf-8') as f:
            listcookies = json.loads(f.read())
        for cookie in listcookies:
            brower.add_cookie(cookie)
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        brower.get(url)
        if page > 1:
            put = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
            submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
            put.clear()
            put.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)

def get_products():
    html = brower.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text(),
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)

if __name__ == '__main__':
    index_page(1)
