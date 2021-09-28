#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 运行语句：export PYTHONIOENCODING=utf-8; python test.py
from model import Model


vocab_file = './data/couplet/vocabs'
model_dir = './models/output_couplet'

m = Model(
        None, None, None, None, vocab_file,
        num_units=1024, layers=4, dropout=0.2,
        batch_size=32, learning_rate=0.0001,
        output_dir=model_dir,
        restore_model=True, init_train=False, init_infer=True)

def get_bot_response(msg):
    inputText = msg
    if len(inputText) == 0:
        output = u'您输入了寂寞～'
    elif len(inputText) > 50:
        output = u'您的对联超过你家的门～'
    else:
        output = m.infer(' '.join(inputText))
        output = ''.join(output.split(' '))
    return str(output)

while True:
    msg = input('请输入您的上联：') # 小小书童可笑可笑
    next = get_bot_response(msg)
    print('下联为：%s'%next)
    print('\n')