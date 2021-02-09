from blockchainData import BlockchainData
class BlockInfos:
    __txHistBinLabels = []
    __txSelectedFee = []
    __txSelectedSize = []
    __feesPerBinPerByte = []
    __feesPerBinPerByteDict = []
    __averageTxSize = {}
    __averageTxSizeProc = {}
    __averagePpbSize = {}
    def __init__(self,binWidth):
        data = BlockchainData()
        self.__binWidth = binWidth
        self.__txs = data.txs
        self.__sizes = data.sizes
        self.__fees = data.fees
        self.__init_data(binWidth)
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
    def __init_data(self,binWidth):
        self.__txHistBinLabels = [self.__getHistBinHeight(i,self.__binWidth) for i in self.__sizes]
        #[dataset][0 bin width,1 indexes]
        #block mit transaktionen
        self.__txSelectedFee = []
        for block in range(0,len(self.__txHistBinLabels)):
            binCluster = []
            #alle bins rausholen
            for binIndexes in list(self.__txHistBinLabels[block][1].values()):
                #aus jeden bin indizes rausholen
                binGroup = []
                for index in binIndexes:
                    binGroup.append(self.__txs[block][index].fee)
                binCluster.append(binGroup)
            self.__txSelectedFee.append(binCluster)

        #[block][Bin] = values
        #block mit transaktionen
        self.__txSelectedSize = []
        for block in range(0,len(self.__txHistBinLabels)):
            binCluster = []
            #alle bins rausholen
            for binIndexes in list(self.__txHistBinLabels[block][1].values()):
                #aus jeden bin indizes rausholen
                binGroup = []
                for index in binIndexes:
                    binGroup.append(self.__txs[block][index].size)
                binCluster.append(binGroup)
            self.__txSelectedSize.append(binCluster)
        self.__feesPerBinPerByte = []
        #block
        for i in range(0,len(self.__txSelectedFee)):
            #bins
            bins = []
            for j in range(0,len(self.__txSelectedFee[i])):
                binValuesFee = self.__txSelectedFee[i][j]
                binValuesSize = self.__txSelectedSize[i][j]
                bins.append(sum(binValuesFee)/sum(binValuesSize))
            #ppb.append(bins)
            self.__feesPerBinPerByte.append(bins)
        self.__feesPerBinPerByteDict = []
        for i in range(0,len(self.__txHistBinLabels)):
            binCat = dict(zip(list(self.__txHistBinLabels[i][0].keys()),self.__feesPerBinPerByte[i]))
            self.__feesPerBinPerByteDict.append(binCat)
        #average fee per byte in all bins

        #todo unite and get kn
        ppbKeys = [list(txDict.keys()) for txDict in self.__feesPerBinPerByteDict]
        inc = 1
        binCount = {binWidth*i:0 for i in range(1,401)}
        binCountSum = {binWidth*i:0 for i in range(1,401)}
        for dictInd in range(len(self.__feesPerBinPerByteDict)):
            for keyTx in ppbKeys[dictInd]:
                if keyTx in binCount:
                    binCount[keyTx] += 1
                    binCountSum[keyTx] += self.__feesPerBinPerByteDict[dictInd][keyTx]
                else:
                    binCount[keyTx] = 1
                    binCountSum[keyTx] = self.__feesPerBinPerByteDict[dictInd][keyTx]
        self.__averagePpbSize = {}
        for i in list(binCount.keys()):
            if binCount[i] != 0:
                self.__averagePpbSize[i] = binCountSum[i]/binCount[i]
        #calculating average transaction count in bin
        #todo unite and get kn
        txSizesKeys = [list(txDict[0].keys()) for txDict in self.__txHistBinLabels]
        inc = 1
        binCount = {binWidth*i:0 for i in range(1,401)}
        #binCount[300] += 1
        binCountSum = {binWidth*i:0 for i in range(1,401)}
        for dictInd in range(len(self.__txHistBinLabels)):
            for keyTx in txSizesKeys[dictInd]:
                if keyTx in binCount:
                    binCount[keyTx] += 1
                    binCountSum[keyTx] += self.__txHistBinLabels[dictInd][0][keyTx]
                else:
                    binCount[keyTx] = 1
                    binCountSum[keyTx] = self.__txHistBinLabels[dictInd][0][keyTx]
        self.__averageTxSize = {}
        for i in list(binCount.keys()):
            if binCount[i] != 0:
                self.__averageTxSize[i] = binCountSum[i]/binCount[i]
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
    #die methode liefert zum einen daten einer histogram und zum andern
    #die indizen von den datenpunkten die sich in den bins befinden damit man dieser wieder zuordnen kann
    # rückgabe [binGrößen,indizen von Daten die in den jeweiligen bins drin sind]
