import pandas as pd

# 读取csv文件
df = pd.read_csv('cleaned_weibo_content_gaokao.csv')
# 保存为xlsx文件
df.to_excel('cleaned_weibo_content_gaokao.xlsx', index=False)