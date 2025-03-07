import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
intent_dict = {
    "play_game": "玩游戏",
    "email_querycontact": "电子邮件查询联系人",
    "general_quirky": "quirky",
    "email_addcontact": "电子邮件添加联系人",
    "takeaway_query": "外卖查询",
    "recommendation_locations": "地点推荐",
    "transport_traffic": "交通运输",
    "iot_cleaning": "物联网-吸尘器, 清洁器",
    "general_joke": "笑话",
    "lists_query": "查询列表/清单",
    "calendar_remove": "日历删除事件",
    "transport_taxi": "打车, 出租车预约",
    "qa_factoid": "事实性问答",
    "transport_ticket": "交通票据",
    "play_radio": "播放广播",
    "alarm_set": "设置闹钟",
}

intent_string = json.dumps(intent_dict,ensure_ascii=False)

system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. 
You should choose one tag from the tag list:
{intent_string}
Just reply with the chosen tag."""


client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
messages = [
    {'role': 'system', 'content': system_prompt},
    {'role': 'user', 'content': "星期五早上九点叫醒我"}
]
response = client.chat.completions.create(
    model="tongyi-intent-detect-v3",
    messages=messages
)

print(response.choices[0].message.content)
