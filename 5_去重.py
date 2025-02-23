from BCEmbedding import EmbeddingModel
import pandas as pd
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

# 读取数据
dataset_label = "/mnt/workspace/melantha1/active_topics/topic_list.json"

with open(dataset_label, "r", encoding='utf-8') as file:
    data = json.load(file)
df_list = pd.DataFrame(data)
LABEL = list(df_list['topics'])

# 加载模型
model = EmbeddingModel(model_name_or_path="/mnt/workspace/melantha1/BCE_1")

for label in LABEL:
    dataset = f"/mnt/workspace/melantha1/AAAAAAAA/cluster_after_process/{label}.json"

    with open(dataset, "r", encoding='utf-8') as file:
        clusters = json.load(file)

    res_list = []

    for cluster in clusters:
        cluster_value = cluster.get("cluster")
        sentences = cluster.get("sentence")
        index = cluster.get("index")

        if cluster_value != -1:
            # 计算嵌入 & 余弦相似度
            embeddings = model.encode(sentences)
            similarity_matrix = cosine_similarity(embeddings)
            normalized_similarity = normalize(similarity_matrix, axis=0, norm='max')

            seen = set()
            unique_content = []
            unique_indices = []

            # 遍历所有内容
            for i in range(len(sentences)):
                if i in seen:
                    continue  # 如果该项已被归为重复项，则跳过

                longest_content = sentences[i]  # 记录当前最长内容
                grouped_indices = [index[i]]

                # 遍历后续的内容，查找重复项
                for j in range(i + 1, len(sentences)):
                    if normalized_similarity[i][j] > 0.99:  # 判定为重复
                        seen.add(j)  # 记录已处理项
                        grouped_indices.append(index[j])

                        # **保留最长的内容**
                        if len(sentences[j]) > len(longest_content):
                            longest_content = sentences[j]

                # 记录唯一内容（最长的）及其索引组
                unique_content.append(longest_content)
                unique_indices.append(list(set(grouped_indices)))  # 去重索引

            # 组织成新的数据结构
            result = {'cluster': cluster_value, 'sentence': unique_content, 'index': unique_indices}
            res_list.append(result)

        else:  # cluster = -1，不需要去重
            result = {'cluster': cluster_value, 'sentence': sentences, 'index': index}
            res_list.append(result)

    # **存储 JSON**
    save_path = f"/mnt/workspace/melantha1/AAAAAAAA/duplicate/{label}.json"
    df = pd.DataFrame(res_list)
    df_json = df.to_json(orient="records", force_ascii=False, indent=4)

    # 处理 JSON 反斜杠问题
    df_json = df_json.replace(r"\/", "/")

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(df_json)

print("所有数据处理完成！")
