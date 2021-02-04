#%%

from blockchain import blockexplorer
from blockchain.blockexplorer import save_block_as_json

block = blockexplorer.get_block('00000000000000000001ed2650c47ae2504dda4762766162ee95aa770f09119d')
save_block_as_json(block)
