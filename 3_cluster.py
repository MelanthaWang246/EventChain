from BCEmbedding import EmbeddingModel
import pandas as pd
import json
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

dataset_label = "/mnt/workspace/melantha1/active_topics/topic_list.json" 

with open(dataset_label, "r", encoding='utf-8') as file:
    data = json.load(file)
df_list = pd.DataFrame(data)
LABEL = list(df_list['topics'])
for label in LABEL:   
    dataset = str("/mnt/workspace/melantha1/active_topics/final/"+str(label)+".json") 
    with open(dataset, "r", encoding='utf-8') as file:
        data = json.load(file)   
    contents_df = pd.DataFrame(data)

    sentences = [] 
    for sentence in contents_df['desc']:
        sentences.append(sentence)
        

    # extract embeddings
    # init embedding model
    model = EmbeddingModel(model_name_or_path="/mnt/workspace/melantha1/BCE_1")
    embeddings = model.encode(sentences)

    similarity_matrix = cosine_similarity(embeddings)
    normalized_similarity = normalize(similarity_matrix, axis=0, norm='max')

    # 将相似度矩阵转换为距离矩阵
    distance_matrix = 1-normalized_similarity

    print("距离矩阵计算结束")
    # np.savetxt("/mnt/workspace/melantha1/AAAAAAAA/distance.txt",distance_matrix)


    # 设置 DBSCAN 参数
    eps = 0.2  # 邻域半径
    min_samples = 5  # 最小样本数

    # 初始化并拟合 DBSCAN 模型
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed').fit_predict(distance_matrix)
    # dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='precomputed').fit(distance_matrix)

    # labels = dbscan.labels_
    # print(labels)
    # contents_df['cluster'] = labels
    contents_df['cluster'] = dbscan
    
    # save_path = str("/mnt/workspace/melantha1/AAAAAAAA/cluster_2/"+str(label)+".json") 
    # contents_df.to_json(save_path, orient="records", force_ascii=False, indent=4)
    
    save_path = str("/mnt/workspace/melantha1/AAAAAAAA/cluster/"+str(label)+".json") 
    # 保存为json文件
    df_json = contents_df.to_json(orient="records", force_ascii=False, indent=4)
    # 处理url值中的 / 被记录为 \/
    df_json = df_json.replace(r"\/", "/")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(df_json)    