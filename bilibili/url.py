import os
import re

# 定义正则表达式匹配Markdown中的超链接
md_link_pattern = r'\[.*?\]\((https?://[^\s]+)\)'

def extract_links_from_md(file_path):
    """从单个MD文件中提取超链接"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        links = re.findall(md_link_pattern, content)
        return links

def extract_links_from_folder(folder_path):
    """从文件夹中的所有MD文件中提取超链接"""
    all_links = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            links = extract_links_from_md(file_path)
            all_links.extend(links)
    return all_links

# 设置MD文件所在的文件夹路径
folder_path = './bilibili'  # 替换为你的MD文件夹路径

# 提取所有超链接
links = extract_links_from_folder(folder_path)

# # 打印或保存结果
# for link in links:
#     print(link)

# 如果需要保存到文件
with open('idlist.txt', 'w', encoding='utf-8') as output_file:
    for link in links:
        output_file.write(link + '\n')