#创建蓝本
from flask import Blueprint

#参数：蓝本的名字和蓝本所在的包和模块
main = Blueprint('main', __name__)

#在末尾导入，是为了避免循环导入依赖
from . import views, errors
