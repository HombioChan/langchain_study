from evaluate.dto import QuestionReq
from evaluate.file_util import read_dataset_excel, ResultRow, write_results_to_excel
from evaluate.http_util import get_answer, clear_session
import time

BUYER_PREFIX = '买家：'
SELLER_PREFIX = '客服：'

def split_chat_log(data_rows: list[str]) -> list[list[str]]:
    result = []
    split_list = []
    for data_row_item in data_rows:
        if data_row_item.startswith(BUYER_PREFIX):
            if len(split_list) > 0:
                result.append(split_list)
            split_list = [data_row_item.replace(BUYER_PREFIX, '')]
        else:
            split_list.append(data_row_item.replace(SELLER_PREFIX, ''))
    return result

if __name__ == "__main__":
    test_third_shop_id = '1901804294533821753'
    test_chat_bot_shop_id = 'SHP928147835494852600163E1274F60'
    # 指定 Excel 文件的路径
    file_path = '../dataset/dataset_clothing_300_1.xlsx'

    # 调用函数读取并打印 Excel 文件内容
    dataset = read_dataset_excel(file_path)

    result_list = []

    for index, row in enumerate(dataset):
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
                # print(result_row)
                # if not ('订单卡片' in ask_method_name
                #         or '宝贝链接' in ask_method_name
                #         or '视频' in ask_method_name
                #         or '音频' in ask_method_name
                #         or '符号' in ask_method_name
                #         or '表情' in ask_method_name
                #         or '图片' in ask_method_name):
                #     result_list.append(result_row)
            context.append(BUYER_PREFIX + buyer_question)
            if len(seller_answers) > 0:
                for seller_answer in seller_answers:
                    context.append(SELLER_PREFIX + seller_answer)
            print(f'index={index}, chat_log_list_size={len(chat_log_list)}, chunks_size={len(chunks)}, idx={idx}')
    write_results_to_excel(result_list, '../result/dataset_clothing_300_1.xlsx')

