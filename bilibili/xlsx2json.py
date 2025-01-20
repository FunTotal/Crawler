import pandas as pd

# 读取xlsx文件
df = pd.read_excel('output.xlsx')
# 保存为json文件
df.to_json('output.json', orient='records', force_ascii=False)