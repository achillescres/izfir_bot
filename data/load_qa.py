import pandas as pd

df = pd.read_csv('raw_data/qu_ans.csv')
df = df.reset_index()
for index, row in df.iterrows():
    print(row['question'])
