from motor.core import AgnosticCollection


REAL_LIMIT = 49
LOWER_LIMIT = 44


async def format_rows(faculties, fac_key, rows):
    new_rows = []
    for i, row in enumerate(rows):
        # print(row)
        row[0] = f"{i+1}. {row[0]}"
        if len(row[0]) <= REAL_LIMIT:
            new_rows.append(row+[i])
            continue

        qu = row[0].split(' ')[::-1]
        parts = []
        while qu:
            part = ''
            while len(part) <= LOWER_LIMIT and qu:
                if len(part) + len(qu[-1]) <= REAL_LIMIT:
                    part += ' ' + qu[-1]
                    qu.pop()
                else:
                    #     part += ' ' + qu[-1]
                    #     part1 = part[:REAL_LIMIT + 1]
                    #     bad_part = part[REAL_LIMIT+1:]
                    #     if bad_part:
                    #         qu.append(bad_part)
                    #     part = part1
                    break

            parts.append([part.strip(), row[1].strip(), i])

        new_rows.extend(parts)

    await faculties.update_one({'faculty.key': fac_key}, {'$set': {'qus_ans_calls': []}})
    for i in new_rows:
        await add_qu_an_call(faculties, {'qu': i[0], 'an': i[1], 'index': i[2]}, fac_key)


async def add_qu_an_call(collection: AgnosticCollection, qu_an_call, to_fac_key: str):
    new_call = f'{to_fac_key}_{qu_an_call["index"]}'
    new_qu_an_call = {
        'not_an_index': qu_an_call['index'],
        'qu': qu_an_call['qu'],
        'an': qu_an_call['an'],
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