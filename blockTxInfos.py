from blockchainData import BlockchainData
class BlockInfos:
    __averageTxSize = {}
    __averageTxSizeProc = {}
    __averagePpbSize = {}
    __avgTimeToConf = {}
    def __init__(self,binWidth):
        self.__data = BlockchainData()
        self.__binWidth = binWidth
        self.__txs = self.__data.txs
        self.__sizes = self.__data.sizes
        self.__fees = self.__data.fees
        self.__init_data()
        self.__statistics()
    def __getHistBinHeight(self,data,binWidth):
        dataDict = {i:data[i] for i in range(0,len(data))}
        dataDict = dict(sorted(dataDict.items(), key=lambda item: item[1]))
        #data = sorted(data)
        binIndexes = {binWidth:[]}
        inc = 1
        binHeights = {}
        counter = 0
        for dataKey in dataDict:
            txsize = dataDict[dataKey]
            currentWidth = binWidth*inc
            if currentWidth not in binIndexes:
                binIndexes[currentWidth] = []
            if txsize < currentWidth:
                counter = counter+1
                binIndexes[currentWidth].append(dataKey)
            elif txsize >= currentWidth and txsize < currentWidth+binWidth:
                inc = inc + 1
                binHeights[currentWidth] = counter
                binIndexes[currentWidth].append(dataKey)
                counter = 1
            else:
                binHeights[currentWidth] = counter
                binIndexes[currentWidth].append(dataKey)
                counter = 1
                inc=self.__determineBin(txsize,binWidth)
                binHeights[binWidth*inc] = counter
                if binWidth*inc not in binIndexes:
                    binIndexes[binWidth*inc] = []
                binIndexes[binWidth*inc].append(dataKey)
        return [binHeights,binIndexes]
    def __determineBin(self,val,binWidth):
        inc = 1
        while val >= binWidth*inc:
            inc = inc + 1
        return inc
    #0 - size 1 - fee 2-time
    def __getTxSelectedBin(self,binLabels,t):
        txSelectedFee = []
        for block in range(0,len(binLabels)):
            binCluster = []
            #alle bins rausholen
            for binIndexes in list(binLabels[block][1].values()):
                #aus jeden bin indizes rausholen
                binGroup = []
                for index in binIndexes:
                    if t == 0:
                        binGroup.append(self.__txs[block][index].size)
                    elif t==1:
                        binGroup.append(self.__txs[block][index].fee)
                    elif t==2:
                        binGroup.append(self.__txs[block][index].time)
                binCluster.append(binGroup)
            txSelectedFee.append(binCluster)
        return txSelectedFee
    def __getFeePerBinPerByte(self,txFee,txSizes):
        feesPerBinPerByte = []
        #block
        for i in range(0,len(txFee)):
            #bins
            bins = []
            for j in range(0,len(txFee[i])):
                binValuesFee = txFee[i][j]
                binValuesSize = txSizes[i][j]
                bins.append(sum(binValuesFee)/sum(binValuesSize))
            feesPerBinPerByte.append(bins)
        return feesPerBinPerByte
    def __computeAveragePpbSize(self,ppbDict):
        #average fee per byte in all bins
        #todo unite and get kn
        ppbKeys = [list(txDict.keys()) for txDict in ppbDict]
        inc = 1
        binCount = {self.__binWidth*i:0 for i in range(1,401)}
        binCountSum = {self.__binWidth*i:0 for i in range(1,401)}
        for dictInd in range(len(ppbDict)):
            for keyTx in ppbKeys[dictInd]:
                if keyTx in binCount:
                    binCount[keyTx] += 1
                    binCountSum[keyTx] += ppbDict[dictInd][keyTx]
                else:
                    binCount[keyTx] = 1
                    binCountSum[keyTx] = ppbDict[dictInd][keyTx]
        averagePpbSize = {}
        for i in list(binCount.keys()):
            if binCount[i] != 0:
                averagePpbSize[i] = binCountSum[i]/binCount[i]
        return averagePpbSize
    def __computeAverageTxSizePerBin(self,txHistBinLabels):
        txSizesKeys = [list(txDict[0].keys()) for txDict in txHistBinLabels]
        inc = 1
        binCount = {self.__binWidth*i:0 for i in range(1,401)}
        #binCount[300] += 1
        binCountSum = {self.__binWidth*i:0 for i in range(1,401)}
        for dictInd in range(len(txHistBinLabels)):
            for keyTx in txSizesKeys[dictInd]:
                if keyTx in binCount:
                    binCount[keyTx] += 1
                    binCountSum[keyTx] += txHistBinLabels[dictInd][0][keyTx]
                else:
                    binCount[keyTx] = 1
                    binCountSum[keyTx] = txHistBinLabels[dictInd][0][keyTx]
        averageTxSize = {}
        for i in list(binCount.keys()):
            if binCount[i] != 0:
                averageTxSize[i] = binCountSum[i]/binCount[i]
        return averageTxSize

    def __computeAvgConfTimePerBin(self,txHistBinLabels):
        txHistIndexes = [i[1] for i in txHistBinLabels]
        blocks = self.__data.blocks
        blockTimes = [block.time for block in blocks]
        blockHeights =[block.height for block in blocks]
        blockHeightTimeDict = dict(list(zip(blockHeights,blockTimes)))
        confTimePerBin = []
        for block in range(0,len(txHistIndexes)):
            binCluster = []
            #alle bins rausholen
            for binDict in txHistIndexes[block]:
                #aus jeden bin indizes rausholen
                binGroup = {}
                timesList = []
                for index in txHistIndexes[block][binDict]:
                    tx = self.__txs[block][index]
                    txBlock = tx.block_height
                    confTime = blockHeightTimeDict[txBlock]-tx.time #zeit in s
                    timesList.append(confTime)
                binGroup[binDict] = timesList
                binCluster.append(binGroup)
            confTimePerBin.append(binCluster)
        #get an average conf time per size
        #return confTimePerBin
        keys = [list(txDict.keys()) for txDict in txHistIndexes]
        inc = 1
        binCount = {self.__binWidth*i:0 for i in range(1,401)}
        binCountSum = {self.__binWidth*i:0 for i in range(1,401)}
        for dictInd in range(0,len(confTimePerBin)):
            dictKeys = list(keys[dictInd])
            for keyTx in range(0,len(dictKeys)):
                if dictKeys[keyTx] in binCount:
                    binCount[dictKeys[keyTx]] += 1
                    confTimes = confTimePerBin[dictInd][keyTx][dictKeys[keyTx]]
                    binCountSum[dictKeys[keyTx]] += sum(confTimes)/len(confTimes)
                else:
                    binCount[dictKeys[keyTx]] = 1
                    binCountSum[dictKeys[keyTx]] = 1
                    confTimes = confTimePerBin[dictInd][keyTx][dictKeys[keyTx]]
                    binCountSum[dictKeys[keyTx]] += sum(confTimes)/len(confTimes)

        avgTimeToConf = {}
        for i in list(binCount.keys()):
            if binCount[i] != 0:
                avgTimeToConf[i] = binCountSum[i]/binCount[i]
        return avgTimeToConf

    def __init_data(self):
        txHistBinLabels = [self.__getHistBinHeight(i,self.__binWidth) for i in self.__sizes]
        #[dataset][0 bin width,1 indexes]
        #block mit transaktionen
        txSelectedFee = self.__getTxSelectedBin(txHistBinLabels,1)
        #[block][Bin] = values
        #block mit transaktionen
        txSelectedSize = self.__getTxSelectedBin(txHistBinLabels,0)

        feesPerBinPerByte = self.__getFeePerBinPerByte(txSelectedFee,txSelectedSize)
        #create dict with indexes as keys
        feesPerBinPerByteDict = []
        for i in range(0,len(txHistBinLabels)):
            binCat = dict(zip(list(txHistBinLabels[i][0].keys()),feesPerBinPerByte[i]))
            feesPerBinPerByteDict.append(binCat)

        #calculating average transaction count in bin
        self.__averagePpbSize = self.__computeAveragePpbSize(feesPerBinPerByteDict)

        self.__averageTxSize = self.__computeAverageTxSizePerBin(txHistBinLabels)

        self.__avgTimeToConf = self.__computeAvgConfTimePerBin(txHistBinLabels)

        txSelectedSize = self.__getTxSelectedBin(txHistBinLabels,2)
    def __statistics(self):
        y_val = self.__averageTxSize.values()
        x_keys = self.__averageTxSize.keys()
        #averageTxSize
        totaltx = sum(self.__averageTxSize.values()) #total avg tx per block
        self.__averageTxSizeProc = {i:self.__averageTxSize[i]/totaltx for i in list(self.__averageTxSize.keys())}
    #first number of bins
    def getAvgTxSizePerBinInProc(self):
        return self.__averageTxSizeProc
    def getAvgPpbSize(self):
        return self.__averagePpbSize
    def getAverageTimeToConf(self):
        return self.__avgTimeToConf
    #die methode liefert zum einen daten einer histogram und zum andern
    #die indizen von den datenpunkten die sich in den bins befinden damit man dieser wieder zuordnen kann
    # ruckgabe binGen,indizen von Daten die in den jeweiligen bins drin sind
