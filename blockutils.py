import requests
import os
import json
from blockchain import blockexplorer

class BlockUtils():
    def __init__(self):
        self.parent = 'blocks'
        if not os.path.isdir('blocks'):
            os.mkdir('blocks')
        try:
            self.local_blocks = [block for block in os.walk('blocks')]
            self.local_blocks = [block[:-5] for block in self.local_blocks[0][2]]
        except:
            self.local_blocks = []


    def writeBlock(self, block):
        height = block['height']
        if height in self.local_blocks:
            None
        else:
            try:
                with open(f'blocks/{height}.json', 'w') as f:
                    json.dump(block, f)
                return 0
            except:
                print("Could not write to disk")
                return 1

#returns json representation of a block or all downloaded blocks
    def getBlock(self,block=None):
        height = block
        try:
            if not block:
                heights = sorted(self.local_blocks)
                heights
                blocks = []
                for height in heights:
                    with open(f'blocks/{height}.json', 'r') as f:
                        blocks.append(blockexplorer.Block(json.load(f)))
                return blocks
            else:
                with open(f'blocks/{height}.json', 'r') as f:
                    return blockexplorer.Block(json.load(f))
        except:
            print(heights)
            print("block not found on disk or other error")
            return None
    def clear(self):
        if os.path.isdir(self.parent):
            try:
                [os.remove(self.parent+'/'+f) for f in list(os.walk(self.parent))[0][2]]
            except:
                print("Error while removing a file")
