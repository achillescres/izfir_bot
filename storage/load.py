with open('dataa.txt') as f:
    rows = f.read().strip().split(';;;')

data = [[part.strip() for part in row.strip().split('|||')] for row in rows if row]
print(*data, sep='\n')

with open('qus_ans.csv', 'w') as f:
    for row in data:
        f.write(';;;'.join(row))
