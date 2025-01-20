import pandas as pd

# 读取CSV文件
input_file = 'weibo_content_gaokao.csv'  # 替换为你的输入文件路径
output_file = 'cleaned_weibo_content_gaokao.csv'  # 替换为你的输出文件路径

# 读取数据
df = pd.read_csv(input_file)

# 去除完全重复的行
df_cleaned = df.drop_duplicates()

# 保存清洗后的数据到新的CSV文件
df_cleaned.to_csv(output_file, index=False)

print(f"数据清洗完成！清洗后的数据已保存到 {output_file}")