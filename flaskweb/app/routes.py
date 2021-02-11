from flask import Flask, request, render_template
from app import app
from testClass import Test
import sys
from blockTxInfos import BlockInfos
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
    test1 = Test(123)
    title="Home"
    return render_template('track.html',**locals())

@app.route('/stats')
def stats():
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
    return render_template('track.html',**locals())
