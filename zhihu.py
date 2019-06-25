import requests,csv,re,time
from urllib.parse import quote,urlencode
from pyquery import PyQuery as pq
from multiprocessing.pool import Pool

'''
question = url1.split('/')[-1] 
q_url = 'https://www.zhihu.com/api/v4/questions/'+question+'/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset=&limit=10&sort_by=default&platform=desktop'
def parse(q_url,headers=headers,proxies=proxies):
    response = requests.get(q_url,headers=headers,proxies=proxies)
    if response.status_code == 200:
        result = response.json()
        if result.get('paging').get('totals'):
            totals = result.get('paging').get('totals')
        else:
            totals = 0
        for item in result.get('data'):
            comment_count = item.get('comment_count')
            voteup_count = item.get('voteup_count')
            print(totals,comment_count,voteup_count)'''

READ_MIN = 2#从csv文件的第N行开始读取
READ_MAX = 10#读取至csv文件的第N行
GROUP_START = 1#初始页数
GROUP_END = 5#读取页数

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
}
proxy = '127.0.0.1:57525'
proxies = {
    'http': 'http://'+proxy,
    'https':'https://'+proxy
}

def get_page(offset,keyword):
    parms = {
        'correction':'1',
        'offset':offset,
        'limit':'20',
        'lc_idx':offset+1,
        'show_all_topics':'0'
    }
    url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q=' + quote(keyword) + '&'+ urlencode(parms)
    try:
        response = requests.get(url,headers=headers,proxies=proxies)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_result(json):
    with open('Z:\data.csv','a') as csvfile2:
        writer = csv.writer(csvfile2)
        if json.get('data'):
            for item in json.get('data'):
                if item.get('object').get('question'):
                    url = item.get('object').get('question').get('url')
                    url = url.replace('api','www')
                    url = url.replace('questions','question')
                    title = item.get('highlight').get('title')
                    title = re.sub('<em>|</em>','',title)
                    result = parse(url)
                    writer.writerow([title,url,result[0],result[1],result[2]])
                    time.sleep(1)

def parse(url,headers=headers,proxies=proxies):
    response = requests.get(url,headers=headers,proxies=proxies)
    if response.status_code == 200:
        html = response.text
        doc = pq(html)
        if doc('.List-headerText'):
            answers = doc('.List-headerText').text()
        else:
            answers = '0个回答'
        items = doc('.NumberBoard-itemValue')
        concern = items[0].text
        views = items[1].text
        return answers,concern,views

def main(offset,keyword):
    json = get_page(offset,keyword)
    get_result(json)

if __name__ == '__main__':
    with open('Z:\胸肌锻炼长尾词_1557551562.csv','r') as csvfile:
        datas = []
        num = 0
        reader = csv.reader(csvfile)
        for row in reader:
            num += 1
            if num > READ_MIN and num < READ_MAX+1:
                datas.append(row[0])

    with open('Z:\data.csv','w') as csvfile2:
        writer = csv.writer(csvfile2)
        writer.writerow(['标题','url','回答数','关注数','浏览数'])

    groups = ([x * 20 for x in range(GROUP_START,GROUP_END+1)])
    pool = Pool()
    for keyword in datas:
        for group in groups:
            pool.apply_async(main,args=(group,keyword))
    pool.close()
    pool.join()
