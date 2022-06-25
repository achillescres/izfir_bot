# with open('data.customsv') as f:
#     rows = dict.fromkeys(['|||'.join(row.strip().split('|||')[:2]) for row in f.read().strip().split(';;;')][:-1], ).keys()
#     rows = [row.strip() + f'|||qu{i}' for i, row in enumerate(rows)]
#
# with open('qus_ans_calls.customsv', 'w+') as f:
#     f.write(';;;'.join(rows))
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from motor.core import AgnosticCollection

with open('qus_ans_calls.customsv', 'r', encoding='utf8') as f:
    rows = [row.split('|||') for row in f.read().split(';;;')]
    logging.info(len(rows))
    new_rows = []
    for row in rows:
        logging.info(row)
        if len(row[0]) <= 87:
            new_rows.append(row + [row[0]])
            continue
        qu = row[0].split(' ')[::-1]
        clones = []
        while qu:
            clone = ''
            while len(clone) <= 69 and qu:
                clone += ' ' + qu[-1]
                qu.pop()

            clones.append([clone.strip(), row[1], row[2], row[0]])
        new_rows.extend(clones)
    logging.info(new_rows)
    # logging.info(*new_rows, sep='\n')

async def add_qu_an(collection: AgnosticCollection, qu_an, to_fac_key: str):
    try:
        new_not_an_index = (await collection.find_one(
            {'faculty.key': to_fac_key},
            {'normal_qus_ans': {'$slice': -1}}
        ))['normal_qus_ans'][0]['not_an_index'] + 1
    except (TypeError, IndexError):
        new_not_an_index = 0

    new_call = f'{to_fac_key}_{new_not_an_index}'
    new_qu_an_call = {
        'not_an_index': new_not_an_index,
        'qu': qu_an['qu'],
        'an': qu_an['an'],
        'call': new_call
    }

    await collection.update_one(
        {
            'faculty.key': to_fac_key
        },
        {
            '$push':
                {
                    'normal_qus_ans': new_qu_an_call
                }
        }
    )
client: AsyncIOMotorClient = AsyncIOMotorClient('localhost', 27017)
db: AsyncIOMotorDatabase = client.izfir
faculties: AsyncIOMotorCollection = db.qus_ans_calls

loop = client.get_io_loop()
for i in rows:
    logging.info(i)
    loop.run_until_complete(add_qu_an(faculties, {'qu': i[0], 'an': i[1]}, '565ee'))
    # with open('new_qus_ans_calls.customsv', 'w', encoding='utf8') as t:
    #     t.write(';;;'.join(new_rows))
