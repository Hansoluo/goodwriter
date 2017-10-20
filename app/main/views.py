#coding:utf-8
#蓝本中定义的程序路由
from flask import render_template
from . import main

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
