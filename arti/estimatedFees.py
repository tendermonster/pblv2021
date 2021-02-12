#reading in data
from blockchain import blockexplorer
from blockutils import BlockUtils
import numpy as np
#estimation
import itertools
import scipy
from numpy import inf
from scipy.stats import norm
from scipy.stats import lognorm
from scipy.stats import mielke
from scipy.stats import iqr

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

"""This class contains methods that estimate fees"""
class FeeEstimation:
    __sizes =[]
    __fees = []
    __txs = []
    __blocks = []
    __medianFees = None
    #median + iqr and median -iqr
    __mpiqr = []
    __mmpiqr = []
    def __init__(self,blockChainData):
        data = blockChainData
        self.__txs = data.txs
        self.__fees = data.fees
        self.__sizes = data.sizes
        self.__statistics()
    #fetch last n blocks from blockchain.com
    def __fetch_blocks(self,fromBlock,n):
        butils = BlockUtils()
        butils.clear()
        status = butils.writeBlock(fromBlock.json)
        blocks = [fromBlock]
        prev = []
        prevHash = None
        for i in range(0,50):
            prevHash=blocks[0].previous_block
            b = blockexplorer.get_block(prevHash)
            blocks.insert(0,b)
            status = butils.writeBlock(b.json)
            prev = b.previous_block
    def __getLatestBlock(self):
        return blockexplorer.get_block(blockexplorer.get_latest_block().hash)
    #Linear regression model used for estimation
    def __estimateLinReg(self,inputData,polyn):
        inputData=np.array(inputData)
        inputData = inputData.reshape(-1, 1)
        y_train, y_test = train_test_split(inputData, test_size=0.3, random_state=0)
        x_train = np.array(list(range(0,len(y_train)))).reshape(-1,1)
        x_test = np.array(list(range(0,len(y_test)))).reshape(-1,1)

        degree=polyn
        linReg=make_pipeline(PolynomialFeatures(degree),LinearRegression());
        linReg.fit(x_train,y_train);
        linReg.score(x_test,y_test);
        return linReg
        #price per byte
    def __statistics(self):
        npSizes = np.array(self.__sizes,dtype="object")
        npFees = np.array(self.__fees,dtype="object")
        pricePerByte = [np.divide(npFees[i],npSizes[i]) for i in range(0,len(npFees))]
        iqrFees = [iqr(pricePerByte[i]) for i in range(0,len(pricePerByte))]
        self.__medianFees = [np.median(pricePerByte[i]) for i in range(0,len(pricePerByte))]
        #median + iqr and median -iqr
        self.__mpiqr = [self.__medianFees[i]+iqrFees[i] for i in range(0,len(iqrFees))]
        self.__mmpiqr = [self.__medianFees[i]-iqrFees[i] for i in range(0,len(iqrFees))]
    def getFeeMin(self):
        minFeeMod = self.__estimateLinReg(self.__mmpiqr,1)
        minFee = minFeeMod.predict(np.array(list(range(0,len(self.__mmpiqr)+1))).reshape(-1,1))
        return minFee[-1]
    def getFeeMax(self):
        maxFeeMod = self.__estimateLinReg(self.__mpiqr,1)
        maxFee = maxFeeMod.predict(np.array(list(range(0,len(self.__mpiqr)+1))).reshape(-1,1))
        return maxFee[-1]
    def getFeeAvg(self):
        avgFeeMod = self.__estimateLinReg(self.__medianFees,1)
        avgFee = avgFeeMod.predict(np.array(list(range(0,len(self.__medianFees)+1))).reshape(-1,1))
        return avgFee[-1]
        #n-number of last blocks
    def refresh(self,n):
        self.__fetch_blocks(__getLatestBlock(),n)
        self.__initData()
    def getSizes(self):
        return self.__sizes
    def getTxs(self):
        return self.__txs
