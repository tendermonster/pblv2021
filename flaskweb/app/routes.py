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
    fees = FeeEstimation()
    print(fees.getFeeAvg())
    blockStuff = BlockInfos(300)
    print(blockStuff.getAvgPpbSize())
    return render_template('stats.html',**locals())

@app.route('/track', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    test1 = Test(12333333333333)
    title="Home"
    return render_template('track2.html',**locals())
