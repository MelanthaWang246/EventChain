import json
import pandas as pd
from transformers import AutoTokenizer
def split_strings_by_length(strings, max_length=20000):
    result = []  # 存储最终的划分结果
    current_group = []  # 当前累积的字符串组
    current_length = 0  # 当前累积的长度
    
    for string in strings:
        string_length = len(tokenizer.encode(string, add_special_tokens=True))
        
        # 如果加入当前字符串后超过 max_length，则新建一个子列表
        if current_length + string_length > max_length:
            result.append(current_group)  # 先保存当前组
            current_group = []  # 重新开始新的组
            current_length = 0  # 重新计算长度
        
        # 加入当前字符串
        current_group.append(string)
        current_length += string_length
    
    # 处理最后一组
    if current_group:
        result.append(current_group)
    
    return result

tokenizer = AutoTokenizer.from_pretrained("/mnt/workspace/pretrain_model/qwen2/qwen/Qwen2.5-14B-Instruct")

dataset_label = "/mnt/workspace/melantha1/active_topics/topic_list.json" 
with open(dataset_label, "r", encoding='utf-8') as file:
    data = json.load(file)
df_list = pd.DataFrame(data)
LABEL = list(df_list['topics'])
for label in LABEL:   
    dataset = str("/mnt/workspace/melantha1/AAAAAAAA/duplicate/"+str(label)+".json") 
    with open(dataset, "r", encoding='utf-8') as file:
        cluster_res = json.load(file) 
        
    # 运行函数
    final_result = []
    for cluster in cluster_res:
        split_result = split_strings_by_length(cluster.get('sentence'))
        temp_value = {"cluster":cluster.get('cluster'),"sentence": split_result,"index":cluster.get('index')}
        final_result.append(temp_value)

    save_path = str("/mnt/workspace/melantha1/AAAAAAAA/slice/" + label + ".json")        
    with open(save_path, "w", encoding="utf-8") as json_file:
        json.dump(final_result, json_file, indent=4, ensure_ascii=False)    
    
    print("完成")