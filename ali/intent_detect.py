import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

intent_string = """
需要商品推荐
咨询商品功能
咨询摄像头可视距离/范围
其他
"""

# 去除首尾的空白字符，并按换行符分割成列表
intent_list = intent_string.strip().split('\n')

# 创建字典，将每个意图字符串和对应的数字下标存入字典中
intent_dict = {index: intent for index, intent in enumerate(intent_list)}

intent_string_1 = json.dumps(intent_dict,ensure_ascii=False)

system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. 
You should choose one tag from the tag list:
{intent_string_1}
Just reply with the chosen tag."""


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
messages = [
    {'role': 'system', 'content': system_prompt},
    {'role': 'user', 'content': "我要声音清楚的监控"}
    ]
response = client.chat.completions.create(
    model="tongyi-intent-detect-v3",
    messages=messages,
    temperature=0
)

res = response.choices[0].message.content
print(res)
print(intent_dict[int(res)])