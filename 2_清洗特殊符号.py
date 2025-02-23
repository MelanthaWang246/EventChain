import json
import pandas as pd
def clear_special_char(sent):
    # 定义要删除的特殊字符
    special_chars = "★☆◆◇▲△▼▽▶●○〇□■☉⊙◎︻︼︽︾〒↑↓¤▓◣◥◢◤→←↘↙⌒∮※ㄨ╬▂▃▄▅▆▇█￥#"
    # 使用 str.translate 删除所有特殊字符
    return sent.translate(str.maketrans('', '', special_chars))


dataset_label = "/mnt/workspace/melantha1/active_topics/topic_list.json" 

with open(dataset_label, "r", encoding='utf-8') as file:
    data = json.load(file)
df_list = pd.DataFrame(data)
LABEL = list(df_list['topics'])
for label in LABEL:   
    dataset = str("/mnt/workspace/melantha1/active_topics/final/"+str(label)+".json") 
    with open(dataset, "r", encoding='utf-8') as file:
        data = json.load(file)   
    df = pd.DataFrame(data)
    df['desc'] = str("该帖子发布时间为") + df['post_create_time'] + str("。") + df['desc']
    df['desc'] = df['desc'].apply(clear_special_char)
    

    save_path = str("/mnt/workspace/melantha1/AAAAAAAA/symbol_clean/" + label + ".json")
    # 保存为json文件
    df_json = df.to_json(orient="records", force_ascii=False, indent=4)
    # 处理url值中的 / 被记录为 \/
    df_json = df_json.replace(r"\/", "/")
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(df_json)