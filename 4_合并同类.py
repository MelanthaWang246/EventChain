import json
import pandas as pd
dataset_label = "/mnt/workspace/melantha1/active_topics/topic_list.json" 

with open(dataset_label, "r", encoding='utf-8') as file:
    data = json.load(file)
df_list = pd.DataFrame(data)
LABEL = list(df_list['topics'])
for label in LABEL:   
    dataset = str("/mnt/workspace/melantha1/AAAAAAAA/cluster/"+str(label)+".json")         

    with open(dataset, "r", encoding='utf-8') as file:
        data = json.load(file) 
    df=pd.DataFrame(data)
    df['index'] = df.index
    
    filtered_df = df[df['cluster'] != -1]
    count = filtered_df.groupby('cluster')[df.columns.difference(['cluster'])].apply(lambda group: list(group.index))
    # remain_df = df[df['cluster'] == -1]
    
    counts=pd.DataFrame({
    'cluster':count.index,
    'index': count.values
    })

    sentences = []
    clusters = []
    indexs = []
    for i in range(len(counts)):
        b = counts.loc[i, 'cluster']
        if b != -1:
            clusters.append(b)
            a = counts['index'][i]
            sentence = []
            index = []
            for b in a:
                sentence.append(df['desc'][b])
                index.append(df['index'][b])
            sentences.append(sentence)
            indexs.append(index)
            
    # remain_df=remain_df[['desc','cluster','index']]
    # remain_df.rename(columns={'desc':'sentence'}, inplace=True)
    
    result = pd.DataFrame({
    'cluster': clusters,
    'sentence': sentences,
    'index': indexs
    })
    # remain_df['index'] = remain_df['index'].apply(lambda x: [x])
    # result = pd.concat([result, remain_df], axis=0, ignore_index=True)
    
    save_path = str("/mnt/workspace/melantha1/AAAAAAAA/cluster_after_process/"+str(label)+".json") 
    # 保存为json文件
    df_json = result.to_json(orient="records", force_ascii=False, indent=4)
    # 处理url值中的 / 被记录为 \/
    df_json = df_json.replace(r"\/", "/")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(df_json)  