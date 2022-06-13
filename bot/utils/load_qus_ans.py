from data.config import BOT_ROOT

# _qus = (
#     ('Сколько стоит штрудель?', '170 рублей', 'qu1'),
#     ('Можно пройти на магистратуру если ты ?', 'Конечно, если...', 'qu2'),
# )


def load_qus_ans():
    with open(str(BOT_ROOT) + '/storage/new_qus_ans_calls.customsv', encoding='utf-8') as f:
        data = [row.split('|||') for row in f.read().split(';;;')]

    return data


def make_qu_to_an_origin(qus_ans_calls):
    return {qu: {'answer': an, 'origin': origin} for (qu, an, call, origin) in qus_ans_calls}
