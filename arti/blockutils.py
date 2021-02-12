import requests
import os
import json
from blockchain import blockexplorer

class BlockUtils():
    def __init__(self):
        self.blocksPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'blocks'))
        if not os.path.isdir(self.blocksPath):
            os.mkdir(self.blocksPath)
        try:
            self.local_blocks = [block for block in os.walk(self.blocksPath)]
            self.local_blocks = [block[:-5] for block in self.local_blocks[0][2]]
        except:
            self.local_blocks = []


    def writeBlock(self, block):
        height = block['height']
        if height in self.local_blocks:
            None
        else:
            try:
                with open(f'{self.blocksPath}/{height}.json', 'w') as f:
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
                blocks = []
                for height in heights:
                    with open(f'{self.blocksPath}/{height}.json', 'r') as f:
                        blocks.append(blockexplorer.Block(json.load(f)))
                return blocks
            else:
                with open(f'{self.blocksPath}/{height}.json', 'r') as f:
                    return blockexplorer.Block(json.load(f))
        except:
            print(heights)
            print("block not found on disk or other error")
            return None
    def clear(self):
        if os.path.isdir(self.blocksPath):
            try:
                [os.remove(self.blocksPath+'/'+f) for f in list(os.walk(self.blocksPath))[0][2]]
            except:
                print("Error while removing a file")
