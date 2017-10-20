# encoding:utf-8
import os

#session需要用的
SECRET_KEY = os.urandom(24)

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'goodwriter'
PASSWORD = '11111111'
HOST = '101.132.133.202'
PORT = '3306'
DATABASE = 'goodwriter'
DB_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

#微信token
WX_TOKEN = '2vX79QF'
