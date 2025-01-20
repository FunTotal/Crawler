from bs4 import BeautifulSoup
import pandas as pd
import random
import requests
import pandas as pd
import time
import random

contents = []
created_times = []
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



headers = {
    'cookie' : '',
    'user-agent': ua,#UserAgent().chrome,
    'Referer':'https://www.zhihu.com/question/654859896/answer/3487198664',
    'x-requested-with': 'XMLHttpRequest'
}

# 读取answer_id.csv文件
df = pd.read_csv('answer_id.csv')

# 提取answer_id列
answer_ids = df['answer_id'].tolist()
cookies = [
    ''
]
batch = 0
for answer_id in answer_ids:
    print('正在爬取answer_id为{answer_id}的数据'.format(answer_id=answer_id))
    url = 'https://www.zhihu.com/question/654859896/answer/{answer_id}'.format(answer_id=answer_id)
    try:
        headers1 = {
        'cookie' : random.choice(cookies),
        'user-agent': random.choice(agent),#UserAgent().chrome,
        'Referer':'https://www.zhihu.com/question/654859896/answer/3487198664',
        'x-requested-with': 'XMLHttpRequest'
        }
        resp = requests.get(url, headers=headers1)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 查找content
        content = soup.find('div', class_='RichContent-inner').text
        contents.append(content)
        time_element = soup.find('span', {'data-tooltip': True})
        if time_element:
            created_time = time_element['data-tooltip'].replace('发布于 ', '')
            created_times.append(created_time)
        else:
            created_times.append('-')
    except Exception as e:
        print(f'爬取answer_id为{answer_id}的数据时出现异常：{e}')
        break
    
    time.sleep(random.randint(1,2))

    # 每爬取500个回答就保存一次数据,保存在不同的文件中
    if len(contents) % 500 == 0:
        new_data = {'answer_id': answer_ids[:len(contents)], 'content': contents, 'created_time' : created_times[:len(contents)]}
        new_df = pd.DataFrame(new_data)
        new_df.to_csv(f'text_{batch}.csv', index=True)
        batch += 1