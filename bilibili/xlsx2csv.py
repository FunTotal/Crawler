import pandas as pd

# 读取xlsx文件
df = pd.read_excel('output.xlsx')
# 保存为csv文件
df.to_csv('output.csv', index=False)