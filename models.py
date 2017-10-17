#encoding:utf-8

from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    wechatid = db.Column(db.String(50))

# 素材表：素材编号、内容、用户编号、编辑时间、标签
class Draft(db.Model):
    __tablename__ = 'drafts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag = db.Column(db.tag)
