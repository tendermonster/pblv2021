from blockutils import BlockUtils
class BlockchainData:
    txs = []
    sizes = []
    fees = []
    def __init__(self):
        self.blocks = self.__getBlocks()
        self.__parseData()
    def __getBlocks(self):
        butils = BlockUtils()
        return butils.getBlock()
    def __parseData(self):
        self.txs = []
        self.sizes = []
        self.fees = []
        #alt[0] ----> neu[-1]
        #transaction data
        self.txs=[block.transactions for block in self.blocks]
        for alltx in self.txs:
            self.sizes.append([tx.size for tx in alltx])
        for alltx in self.txs:
            self.fees.append([tx.fee for tx in alltx])
