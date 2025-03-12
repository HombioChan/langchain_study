import time
import re

from evaluate.dto import QuestionReq
from evaluate.file_util import read_dataset_excel, ResultRow, write_results_to_excel
from evaluate.http_util import get_answer, clear_session

BUYER_PREFIX = '买家：'
SELLER_PREFIX = '客服：'

def split_chat_log(data_rows: list[str]) -> list[list[str]]:
    result = []
    split_list = []
    for data_row_item in data_rows:
        idx = data_row_item.index("#")
        data_row_item = data_row_item[idx + 1:]
        if data_row_item.startswith(BUYER_PREFIX):
            if len(split_list) > 0:
                result.append(split_list)
            split_list = [data_row_item.replace(BUYER_PREFIX, '')]
        else:
            split_list.append(data_row_item.replace(SELLER_PREFIX, ''))
    return result

if __name__ == "__main__":
    test_chat_bot_shop_id_1 = 'SHP599551941206130500163E152B540' # 1901804294533821712 呼啦玛卡巴卡
    test_chat_bot_shop_id_2 = 'SHP9875025093853284E2788967982F1' # 2093416804672735573 cececece
    test_chat_bot_shop_arr = [test_chat_bot_shop_id_1, test_chat_bot_shop_id_2]

    # 指定 Excel 文件的路径
    file_path = '../dataset/dataset_3c_100_1.xlsx'

    # 调用函数读取并打印 Excel 文件内容
    dataset = read_dataset_excel(file_path)

    result_list = []

    start = 0
    batch_size = 5
    for index, row in enumerate(dataset):
        if index < start:
            continue
        if index >= start + batch_size:
            break
        for test_chat_bot_shop_id in test_chat_bot_shop_arr:
            clear_session(chat_bot_shop_id=test_chat_bot_shop_id)
        chat_log_list = row.chat_log.split('Đ')
        chunks = split_chat_log(chat_log_list)
        print(f'index={index}, chat_log_list_size={len(chat_log_list)}, chunks_size={len(chunks)}')
        context = []
        for idx, chunk in enumerate(chunks):
            buyer_question = chunk[0]
            if len(chunk) > 1:
                seller_answers = chunk[1:]
            else:
                seller_answers = []
            result_row_list = []
            for test_chat_bot_shop_id in test_chat_bot_shop_arr:
                question_req = QuestionReq(test_chat_bot_shop_id, buyer_question, seller_answers)
                start_ts = int(time.time() * 1000)
                answer_rsp = get_answer(question_req)
                cost_ts = int(time.time() * 1000) - start_ts
                if answer_rsp is not None:
                    ask_method = answer_rsp.askMethod
                    ask_method_name = '未识别'
                    if ask_method is not None:
                        ask_method_name = ask_method['name']
                    rewrite_question = answer_rsp.rewriteQuestion
                    if rewrite_question is None:
                        rewrite_question = answer_rsp.originQuestion
                    result_row = ResultRow(context[:], answer_rsp.originQuestion, rewrite_question, ask_method_name, cost_ts)
                    result_row_list.append(result_row)
            if len(result_row_list) == 0:
                continue
            mam = result_row_list[0].match_ask_method
            if ("宝贝" not in mam
                    and "订单" not in mam
                    and "图片" not in mam
                    and "音频" not in mam
                    and "视频" not in mam
                    and "符号" not in mam
                    and "表情" not in mam):
                result_list.append(result_row_list)
            context.append(BUYER_PREFIX + buyer_question)
            if len(seller_answers) > 0:
                for seller_answer in seller_answers:
                    context.append(SELLER_PREFIX + seller_answer)
            print(f'index={index}, chat_log_list_size={len(chat_log_list)}, chunks_size={len(chunks)}, idx={idx}')
    write_results_to_excel(result_list, '../result/dataset_3c_100_8.xlsx')

