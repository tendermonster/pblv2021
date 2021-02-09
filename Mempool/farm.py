#!/usr/bin/python3 

from time import sleep
import time
import requests
import json


def farm_data():
    while True:
        handle_transactions()
        sleep(30)
        handle_blocks()
        sleep(270)
         
        
def handle_transactions():
    try:
        mempool = requests.get('https://mempool.space/api/mempool')
    except:
        print(f'{getTimeString()}: handle_transactions fehlgeschlagen.')
        return
        
    if mempool.status_code == 200:
        j = mempool.json()
        json_dump(j, f"./mempool/{getTimeString()}")
        with open("amount_transactions.csv", "a") as f:
            f.write(getTimeString() + ",")
            f.write(str(j['count']))
            f.write("\n")
    else:
        print(f'{getTimeString()}: handle_transactions fehlgeschlagen. Fehlercode: {mempool.status_code}')
    
    
def handle_blocks():
    
    try:
        latest_block_req = requests.get('https://mempool.space/api/blocks/tip/hash')
    except:
        print(f'{getTimeString()}: handle_blocks fehlgeschlagen bei /tip/hash.')
        return
    
    if latest_block_req.status_code != 200:
        print(f"handle_blocks /tip/hash fehlgeschlagen mit Status code {latest_block_req.status_code}")
        return
    
    latest_block = latest_block_req.content.decode()
    
    with open('locallatestblock', 'r') as f:
        local_latest_block = f.read()
        
    if local_latest_block != latest_block:
        sleep(30)
        try:
            url = f'https://mempool.space/api/block/{latest_block}'
            block = requests.get(url)
        except:
            print(f'{getTimeString()}: handle_blocks fehlgeschlagen bei /block')
            return
        
        if block.status_code != 200:
            print(f"Blockdownload fehlgeschlagen mit Status code {block.status_code}")
            return
        
        json_dump(block.json(), f"./blocks/{latest_block}.json")
        
        with open("tx_per_block.csv", "a") as f:
            f.write(block.json()['id'] + ",")
            f.write(str(block.json()['timestamp']) + ",")
            f.write(str(block.json()['tx_count']))
            f.write("\n")
            
        with open('locallatestblock', 'w') as f:
            f.write(latest_block)
        
    
def getTimeString():
    return time.strftime("%Y.%m.%d_%H:%M", time.localtime())
            
            
def json_dump(obj, file_name):
    with open(file_name, "w") as f:
        json.dump(obj, f)
    

if __name__ == "__main__":
    farm_data()