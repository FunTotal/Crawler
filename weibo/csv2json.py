import pandas as pd

# 读取csv文件
df = pd.read_csv('cleaned_weibo_content_gaokao.csv')
# 保存为json文件
df.to_json('cleaned_weibo_content_gaokao.json', orient='records', force_ascii=False)