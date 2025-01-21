# 假设文件名为 'actions.txt'
file_path = 'actions.txt'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# 分割句子
sentences = content.split('\n\n\n')  # 使用句号作为分隔符

# 筛选包含两个句号的句子
count_with_two_dots = sum(1 for sentence in sentences if sentence.count('.') >= 2)
total_sentences = len(sentences)

# 计算比例
if total_sentences > 0:
    proportion = count_with_two_dots / total_sentences
else:
    proportion = 0

print(f"包含两个句号的句子数量: {count_with_two_dots}")
print(f"总句子数量: {total_sentences}")
print(f"所占比例: {proportion:.2%}")