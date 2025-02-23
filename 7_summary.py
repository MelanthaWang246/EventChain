from openai import OpenAI
import time
import os
import json
import pandas as pd
from tqdm import tqdm
from prompt import prompt_summarizer


openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

def get_model_res(input_message):
    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    chat_response = client.chat.completions.create(
        model="Qwen2.5-14B-Instruct",
        messages=input_message,
        temperature=0.1,
        top_p=0.8,
        max_tokens=1000,
        extra_body={
            "repetition_penalty": 1.05,
        },
    )
    response = chat_response.choices[0].message.content
    return response

def prompt_result(sentence):
    summary_prompt = prompt_summarizer.format(summarizer_content=sentence) 
    summary_message = [
            {"role": "system", "content": summary_prompt}
        ]
    return get_model_res(summary_message)

dataset_label = "/mnt/workspace/melantha1/active_topics/topic_list.json" 

with open(dataset_label, "r", encoding='utf-8') as file:
    data = json.load(file)
df_list = pd.DataFrame(data)
LABEL = list(df_list['topics'])


for label in LABEL:   
    cluster_path = str("/mnt/workspace/melantha1/AAAAAAAA/slice/"+str(label)+".json") 

    data_list = []
    summary = []
    with open(cluster_path, 'r', encoding='utf-8') as f:
        cluster_res = json.load(f)
        
    for cluster in cluster_res:
        sentences = cluster.get('sentence')
        if len(sentences) > 1:
            summary_res_temp = []
            for sentence in sentences:
                summary_res_temp.append(prompt_result(sentence))
            summary_res = prompt_result(summary_res_temp)
            
            # print('总结结果： \n')
            # print(summary_res)
            temp_value = {"cluster":cluster.get('cluster'),"summary": summary_res,"index":cluster.get('index')}
            data_list.append(temp_value)
            summary.append(summary_res)
        else:
            summary_res = prompt_result(sentences)
                
            # print('总结结果： \n')
            # print(summary_res)
            temp_value = {"cluster":cluster.get('cluster'),"summary": summary_res,"index":cluster.get('index')}
            data_list.append(temp_value)
            summary.append(summary_res)
            
    final_summary_res = prompt_result(summary)    
    final_summary = {'trend':label,"final_summary": final_summary_res}
        
    # 将 data_list 转换为 pandas DataFrame
    df = pd.DataFrame(data_list)

    # 保存为 json 文件
    res_file = str("/mnt/workspace/melantha1/AAAAAAAA/summary_cluster/"+str(label)+".json") 
    df.to_json(res_file, orient="records", force_ascii=False, indent=4)

    
    final_res_file = str("/mnt/workspace/melantha1/AAAAAAAA/summary/final_summary.json") 
    try:
        with open(final_res_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)  # 读取已有数据
            if not isinstance(existing_data, list):  # 确保 JSON 是一个列表
                existing_data = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []  # 文件不存在或解析失败时，初始化为空列表

    # 追加新数据
    existing_data.append(final_summary)

    # 保存回 JSON 文件
    with open(final_res_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(label)    
   