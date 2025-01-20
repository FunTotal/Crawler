import pandas as pd
import glob
import os

# 设置包含CSV文件的文件夹路径
path = r"./csv"  # 修改为您的CSV文件所在路径

# 使用glob获取所有csv文件的列表
all_files = glob.glob(os.path.join(path, "*.csv"))

# 创建一个空列表来存储每个CSV文件的数据
li = []

for filename in all_files:
    # 读取CSV时忽略第一列(如果它是索引列)
    df = pd.read_csv(filename, index_col=None)
    # 如果存在unnamed列(由index=True产生的列)，则删除
    unnamed_cols = [col for col in df.columns if 'Unnamed' in col]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)
    li.append(df)

# 合并所有数据框
frame = pd.concat(li, axis=0, ignore_index=True)

# 显示去重前的行数
print(f"去重前的行数: {len(frame)}")

# 去除完全重复的行
frame_clean = frame.drop_duplicates()

# 显示去重后的行数
print(f"去重后的行数: {len(frame_clean)}")

# 1. CSV格式
frame_clean.to_csv("cleaned_data.csv", index=False)
# 2. Excel格式
frame_clean.to_excel("cleaned_data.xlsx", index=False)
# 3. JSON格式
frame_clean.to_json("cleaned_data.json", orient="records", force_ascii=False)