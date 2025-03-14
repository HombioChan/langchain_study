import pandas as pd


class DatasetRow:
    def __init__(self, context_id: str, buyer_account: str, chat_log: str):
        self.context_id = context_id
        self.buyer_account = buyer_account
        self.chat_log = chat_log

    def __repr__(self):
        return f"DatasetRow(context_id={self.context_id}, buyer_account={self.buyer_account}, chat_log={self.chat_log})"

class ResultRow:
    def __init__(self, context: list[str], question: str, rewrite_question: str, match_ask_method: str, recall_ask_method:[], rerank_ask_method:[], cost_ts: int):
        self.context = context
        self.question = question
        self.rewrite_question = rewrite_question
        self.recall_ask_method = recall_ask_method
        self.rerank_ask_method = rerank_ask_method
        self.match_ask_method = match_ask_method

        self.cost_ts = cost_ts

    def __str__(self):
        return f"ResultRow(context={self.context}, question={self.question}, rewrite_question={self.rewrite_question}, match_ask_method={self.match_ask_method}, cost_ts={self.cost_ts})"

def read_dataset_excel(file_path):
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path)

        # 检查列名是否匹配
        required_columns = {'context_id', 'buyer_account', 'chat_log'}
        if not required_columns.issubset(df.columns):
            raise ValueError(f"Excel 文件缺少必要的列: {required_columns - df.columns}")

        # 将每一行数据转换为 DatasetRow 对象，并存储到列表中
        dataset_rows = [
            DatasetRow(
                context_id=row['context_id'],
                buyer_account=row['buyer_account'],
                chat_log=row['chat_log']
            )
            for index, row in df.iterrows()
        ]
        return dataset_rows
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return []

def write_results_to_excel(results, output_file_path):
    try:
        # 将 ResultRow 对象列表转换为字典列表
        results_dict = [
            {
                'context': '\n'.join(result_2[0].context),
                'question': result_2[0].question,
                'rewrite_question_new': result_2[0].rewrite_question,
                'recall_ask_method_list': '\n'.join(result_2[0].recall_ask_method),
                'rerank_ask_method_list': '\n'.join(result_2[0].rerank_ask_method),
                'match_ask_method_new': result_2[0].match_ask_method,
                'rewrite_question_old': result_2[1].rewrite_question,
                'match_ask_method_old': result_2[1].match_ask_method,
                'new_old_equals' : 1 if result_2[0].match_ask_method == result_2[1].match_ask_method else 0,
                # 'cost_ts_new': result_2[0].cost_ts,
                # 'cost_ts_old': result_2[1].cost_ts
            }
            for result_2 in results
        ]
        # 创建 DataFrame
        df = pd.DataFrame(results_dict)

        # 将 DataFrame 写入 Excel 文件
        df.to_excel(output_file_path, index=False)
        print(f"结果已成功写入到 {output_file_path}")
    except Exception as e:
        print(f"写入文件时出错: {e}")