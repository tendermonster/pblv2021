#!/usr/bin/python3

import pandas as pd

df = pd.read_csv('tx_per_block.csv')
df = df.sort_values('timestamp')

with open('tx_per_block.csv', 'w') as f:
    f.write('id,timestamp,tx_count\n')
    for block in range(len(df)):
        f.write(str(df.iloc[block].id) + "," + str(df.iloc[block].timestamp) + "," + str(df.iloc[block].tx_count))
        f.write("\n")