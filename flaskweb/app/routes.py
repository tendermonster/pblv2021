from flask import Flask, request, render_template
from app import app
from testClass import Test
import sys
from blockTxInfos import BlockInfos
from Mempool import Blockdifference, TransactionsMempool, TransactionsBlock, NewTransactions
from testClass import Test
from blockutils import BlockUtils
from estimatedFees import FeeEstimation
from blockTxInfos import BlockInfos
from blockchainData import BlockchainData
import pandas as pd
import numpy as np
data = BlockchainData()
fees = FeeEstimation(data)
blockStuff = BlockInfos(300,data)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/track')
def track():
    b = Blockdifference()
    test1 = Test(123)
    title = b.tx_pro_block()
    return render_template('track.html',**locals())

@app.route('/stats')
def stats():
    block = Blockdifference()
    tm = TransactionsMempool()
    tb = TransactionsBlock()
    nt = NewTransactions()
    martendata = [int(round(tm.get_median(), 0)), int(round(tb.get_median(), 0)), round(block.get_avg() / 60, 2), int(round(nt.get_avg(), 0)), nt.get_10_cmp()]
    #pass this BlockchainData object to help performance
    feeMinAvgMax = {}
    feeMinAvgMax['min']=fees.getFeeMin()
    feeMinAvgMax['avg']=fees.getFeeAvg()
    feeMinAvgMax['max']=fees.getFeeMax()
    procOfAllTxPerBin = blockStuff.getAvgTxSizePerBinInProc()
    ppbPerBin = blockStuff.getAvgPpbSize()
    confTimePerBin = blockStuff.getAvgTimeToConf()
    c0 = list(ppbPerBin.keys())
    c1 = list(procOfAllTxPerBin.values())
    c2 = list(ppbPerBin.values())
    c3 = list(confTimePerBin.values())
    #c0 = [i for i in range(0,250)]
    #c1 = [i for i in range(0,250)]
    #c2 = [i for i in range(0,250)]
    #c3 = [i for i in range(0,250)]
    print(len(c0),len(c1),len(c2),len(c3))
    histFrame = pd.DataFrame({'bins in byte':c0,'proc of tx':c1,'ppb':c2,'conf time in s':c3})
    histFrame.set_index(["bins in byte"],inplace=True)
    tables=[histFrame.to_html(classes='data',header="true")]
    titles=histFrame.columns.values
    #create pandas html
    return render_template('stats.html',**locals())

@app.route('/track', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    test1 = Test(12333333333333)
    title="Home"
    return render_template('track2.html',**locals())
