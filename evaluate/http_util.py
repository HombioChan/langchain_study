import os

import requests
from dotenv import load_dotenv
from evaluate.dto import AnswerRsp, QuestionReq

load_dotenv()
QA_IP = os.getenv('QA_IP')

def get_answer(question_req: QuestionReq) -> AnswerRsp | None:
    try:
        url = f'http://{QA_IP}:8080/api/test-robot/qa'
        payload = question_req.to_json()
        # 设置请求头
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=payload, headers=headers)
        # 检查响应状态码
        if response.status_code == 200:
            json_res = response.json()
            success = json_res['success']
            if success:
                data_list = json_res['data']
                data_first = data_list[0]
                answer_rsp = AnswerRsp(**data_first)
                return answer_rsp
            else:
                print(f"请求失败，状态码: {response.status_code}")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"请求时出错: {e}")
        return None


def clear_session(chat_bot_shop_id: str) :
    try:
        url = f'http://{QA_IP}:8080/api/test-robot/clear/session/{chat_bot_shop_id}'
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data={}, headers=headers)
        if response.status_code == 200:
            json_res = response.json()
            success = json_res['success']
            if not success:
                print(f"请求失败，状态码: {response.status_code}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"请求时出错: {e}")
