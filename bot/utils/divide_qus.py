from motor.core import AgnosticCollection


REAL_LIMIT = 49
LOWER_LIMIT = 27


async def format_rows(faculties, fac_key, rows):
    new_rows = []
    for row in rows:
        print(row)
        if len(row[0]) <= REAL_LIMIT:
            new_rows.append(row)
            continue

        qu = row[0].split(' ')[::-1]
        parts = []
        while qu:
            part = ''
            while len(part) <= LOWER_LIMIT and qu:
                if len(part) + len(qu[-1]) > REAL_LIMIT:
                    part += ' ' + qu[-1]
                    qu.pop()
                break

            parts.append([part.strip(), row[1].strip()])

        new_rows.extend(parts)

    faculties.update_one({'faculty.key': fac_key}, {'$set': {'qus_ans_calls': []}})
    for i in new_rows:
        await add_qu_an(faculties, {'qu': i[0], 'an': i[1]}, fac_key)


async def add_qu_an(collection: AgnosticCollection, qu_an, to_fac_key: str):
    try:
        new_not_an_index = (await collection.find_one(
            {'faculty.key': to_fac_key},
            {'qus_ans_calls': {'$slice': -1}}
        ))['qus_ans_calls']['not_an_index'] + 1
    except:
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
                    'qus_ans_calls': new_qu_an_call
                }
        }
    )