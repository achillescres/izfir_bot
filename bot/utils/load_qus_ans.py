from bot.data.config import PROJECT_ROOT


def load_qus_ans():
    with open(str(PROJECT_ROOT) + '/storage/data.customsv') as f:
        data = [i.split('|||') for i in f.read().strip().split(';;;')][:-1]

    return data


def make_qu_to_an(qus_ans_calls):
    return {qu: an for (qu, an, call) in qus_ans_calls}

# print(load_qus_ans().values())
