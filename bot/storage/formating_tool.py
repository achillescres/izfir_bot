# with open('data.customsv') as f:
#     rows = dict.fromkeys(['|||'.join(row.strip().split('|||')[:2]) for row in f.read().strip().split(';;;')][:-1], ).keys()
#     rows = [row.strip() + f'|||qu{i}' for i, row in enumerate(rows)]
#
# with open('qus_ans_calls.customsv', 'w+') as f:
#     f.write(';;;'.join(rows))

with open('qus_ans_calls.customsv', 'r') as f:
    rows = [row.split('|||') for row in f.read().split(';;;')]

    new_rows = []
    for row in rows:
        if len(row[0]) <= 87:
            new_rows.append('|||'.join(row + [row[0]]))
            continue
        qu = row[0].split(' ')[::-1]
        clones = []
        while qu:
            clone = ''
            while len(clone) <= 69 and qu:
                clone += ' ' + qu[-1]
                qu.pop()

            clones.append('|||'.join([clone.strip(), row[1], row[2], row[0]]))
        new_rows.extend(clones)

    print(*new_rows, sep='\n')
    with open('new_qus_ans_calls.customsv', 'w') as t:
        t.write(';;;'.join(new_rows))
