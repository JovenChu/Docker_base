#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask, jsonify, request, render_template, Markup, url_for
from app.model import Model
import logging

from app import app
# windows上运行
# vocab_file = './app/data/couplet/vocabs'
# model_dir = './app/models/output_couplet'

# linux上运行
vocab_file = '/code/project/app/data/couplet/vocabs'
model_dir = '/code/project/app/models/output_couplet'

m = Model(
        None, None, None, None, vocab_file,
        num_units=1024, layers=4, dropout=0.2,
        batch_size=32, learning_rate=0.0001,
        output_dir=model_dir,
        restore_model=True, init_train=False, init_infer=True)


@app.route("/Chinese_Couplet")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    inputText = request.args.get("msg")
    if len(inputText) == 0:
        output = u'您输入了寂寞～'
    elif len(inputText) > 50:
        output = u'您的对联超过你家的门～'
    else:
        output = m.infer(' '.join(inputText))
        output = ''.join(output.split(' '))
    # 用Markup方法对HTML文档进行标记，并将其转化为str类型
    # 其目的是为了防止XSS攻击，确保文档安全。
    resText = Markup(output)
    return str(resText)

# @app.route('/Chinese_Couplet', methods=['GET', 'POST'], strict_slashes=False)
# def demo():
#     if request.method == 'GET':
#         return render_template('index.html', input_text='', res_text='')
#     else:
#         inputText = request.form.get("input_text")
#         if len(inputText) == 0:
#             output = u'您输入了寂寞～'
#         elif len(inputText) > 50:
#             output = u'您的对联超过你家的门～'
#         else:
#             output = m.infer(' '.join(inputText))
#             output = ''.join(output.split(' '))
#         # 用Markup方法对HTML文档进行标记，并将其转化为str类型
#         # 其目的是为了防止XSS攻击，确保文档安全。
#         resText = Markup(output)
#         return render_template('index.html', input_text=inputText, res_text=resText)


# 本地直接启动服务并持久化
# http_server = WSGIServer(('', 5500), app)
# http_server.serve_forever()

# 本地访问链接：http://localhost:5500/Chinese_Couplet
# https://10.74.149.11:5500/Chinese_Couplet


# @app.route('/', methods=['GET', 'POST'])
# def demo():
#   if request.method == 'GET':
#     return render_template('index2.html', input_text = '', res_text = '')
#   else:
#     inputText = request.form.get("input_text")
#     resText = Markup(formatRes(reverseText(inputText)))
#     return render_template('index2.html', input_text = inputText, res_text = resText)
