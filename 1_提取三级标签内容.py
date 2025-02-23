import json
import pandas as pd


dataset_label = "/mnt/workspace/melantha1/active_topics/topic_list.json" 

with open(dataset_label, "r", encoding='utf-8') as file:
    data = json.load(file)
df_list = pd.DataFrame(data)

LABEL = list(df_list['topics'])

#################################### 提取帖子内容 ###############
row_value_f = []
row_value_f4 = []

label1st = "media_info"
for label in LABEL:
    dataset = str("/mnt/workspace/melantha1/active_topics/"+str(label)+".json") 
    with open(dataset, "r", encoding='utf-8') as file:
        data = json.load(file)

    records = []   
    media_info = data.get(label1st, {})
    for label2nd, details in media_info.items():
        record = {"label2nd": label2nd}
        record.update(details)
        records.append(record)

    media_df = pd.DataFrame(records)
    
    
    # # 保存路径
    # save_path = str("/mnt/workspace/melantha1/active_topics/" + label1st + "/" + label + ".json")


    # # 保存为json文件
    # media_json = media_df.to_json(orient="records", force_ascii=False, indent=4)
    # # 处理url值中的 / 被记录为 \/
    # media_json = media_json.replace(r"\/", "/")
    # with open(save_path, "w", encoding="utf-8") as f:
    #     f.write(media_json)
        
    save_df = media_df[['url','desc', 'title', 'content','nickname', 'platform', 'post_create_time']]
    save_path = str("/mnt/workspace/melantha1/active_topics/final/" + label + ".json")


    # 保存为json文件
    media_json = save_df.to_json(orient="records", force_ascii=False, indent=4)
    # 处理url值中的 / 被记录为 \/
    media_json = media_json.replace(r"\/", "/")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(media_json)