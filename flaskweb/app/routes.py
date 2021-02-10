from flask import Flask, request, render_template
from app import app
from testClass import Test
import sys

@app.route('/')
@app.route('/index')
def index():
    test1 = Test(123)
    title="Home"
    return render_template('index.html',**locals())

@app.route('/form')
def myform():
    return render_template('my-form.html')

@app.route('/form', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    test1 = Test(12333333333333)
    title="Home"
    return render_template('index.html',**locals())
