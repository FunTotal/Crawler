import requests
import pandas as pd
import time
import random

template = 'https://www.zhihu.com/api/v4/questions/656533798/feeds?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B*%5D.author.follower_count%2Cvip_info%2Ckvip_info%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings.table_of_content.enabled&offset={offset}&limit=3&order=default&ws_qiangzhisafe=1&platform=desktop'



df = pd.DataFrame()
# df有三列，answer_id和content以及创建日期
df['answer_id'] = []
df['content'] = []
df['created_time'] = []

answer_ids = []

agent = [
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
            'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Mobile Safari/537.36'
        ]
ua = random.choice(agent)

cookies = [
    ''
]
cookie = random.choice(cookies)
headers = {
    'cookie' : cookie,
    'user-agent': ua,#UserAgent().chrome,
    'Referer':'https://www.zhihu.com/question/654859896/answer/3487198664',
    'x-requested-with': 'XMLHttpRequest'
}


# 第一条使用模版，后面的都是next来获取
url0 = template.format(offset=0)
resp0 = requests.get(url0, headers=headers)
for data in resp0.json()['data']:
        answer_id = data['target']['id']
        answer_ids.append(answer_id)
next = resp0.json()['paging']['next']

for page in range(1,5001):# 这里自己估算一下，每页是5条数据
    #对第page页进行访问
    headers1 = {
    'cookie' : random.choice(cookies),
    'user-agent': random.choice(agent),#UserAgent().chrome,
    'Referer':'https://www.zhihu.com/question/654859896/answer/3487198664',
    'x-requested-with': 'XMLHttpRequest'
    }
    resp = requests.get(next, headers=headers1)
    print('正在爬取第' + str(page) + '页')
    
    for data in resp.json()['data']:
        answer_id = data['target']['id']
        # 添加answer_id到df中
        answer_ids.append(answer_id)
    next = resp.json()['paging']['next']
    time.sleep(random.randint(1,4))
    # 每隔100条保存一次信息
    if (page % 100 == 0):
        df = pd.DataFrame({'answer_id': answer_ids})  # 重新创建df
        df.to_csv('answer_id.csv', index=True)