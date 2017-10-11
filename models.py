#encoding:utf-8

from exts import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    wechatid = db.Column(db.String(50))
