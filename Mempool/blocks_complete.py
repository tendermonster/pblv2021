#!/usr/bin/python3

import os
import json

files = [i for i in os.walk("./blocks")][0][2]
files_raw = [i[:-5] for i in files]
prev = []
prev_and_next = {}
missing = []
block_to_time = {}
for file in files:
    with open(f'./blocks/{file}', 'r') as f:
        block = json.load(f)
        prev_and_next[block["previousblockhash"]] = block['id']
        prev.append(block["previousblockhash"])
        block_to_time[block['id']] = block['timestamp']
        
missing = [i for i in prev if i not in files_raw]
min_time = min([i for i in block_to_time.values()])
min_block = ""

for key in block_to_time.keys():
    if block_to_time[key] == min_time:
        min_block = key
        
        
for i in prev_and_next.keys():
    if prev_and_next[i] == min_block:
        missing.remove(i)    

print("Fehlende Blöcke:")
for i in missing:
    print(i)