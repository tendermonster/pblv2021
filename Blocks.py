#!/usr/bin/python3

import requests
import os
import json

class Blocks():
    
    def __init__(self):
        self.block_path = "full_blocks"
        if not os.path.isdir(self.block_path):
            os.mkdir(self.block_path)
        try:
            self.local_blocks = [block for block in os.walk(self.block_path)]
            self.local_blocks = [block[:-5] for block in self.local_blocks[0][2]]
        except: 
            self.local_blocks = []
    
    
    def getBlock(self, block):
        if block in self.local_blocks:
            with open(f'{self.block_path}/{block}.json', 'r') as f:
                return json.load(f)
        else:
            url = f'https://blockchain.info/rawblock/{block}'
            r = requests.get(url)
            if r.status_code != 200:
                raise ValueError('Fehler beim Downloaden')
            with open(f'{self.block_path}/{block}.json', 'w') as f:
                json.dump(r.json(), f)
            self.local_blocks.append(block)
            return r.json()