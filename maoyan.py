import requests,re,json,time
def get_page(url):
    headers = {'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
               '/73.0.3683.103 Safari/537.3'}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>\
        .*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S
    )
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'title':item[2].strip(),
            'actor':item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time':item[4].strip()[5:] if len(item[4]) > 5 else '',
        }

def write(text):
    with open('result.txt','a') as f:
        f.write(json.dumps(text) + '\n')

def main(offset):
    url = 'http://maoyan.com/board/4' + str(offset)
    html = get_page(url)
    for item in parse_page(html):
        write(item)

if __name__ == '__main__':
    for i in range(10):
        main(i*10)
