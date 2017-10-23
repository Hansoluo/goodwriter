from flask import Flask,render_template,redirect,url_for,session,request,make_response
import xml.etree.ElementTree as ET
import config
from models import User,Material,Article
from app import db
from app import app
from app.wx import valication, reply_text
from datetime import datetime
from sqlalchemy import desc

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/regist/', methods=['GET','POST'])
def regist():
    """注册页面"""
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form['email']
        wechatid = request.form['wechatid']
        password1 = request.form['password1']
        password2 = request.form['password2']

        #邮箱验证，如果被注册了，就不能再注册了
        user = User.query.filter(User.email == email).first()
        if user:
            return u'该邮箱已被注册，请更换邮箱注册'
        else:
            # 验证password1和password2是否相等
            if password1 != password2:
                return u'两次密码不相等，请核对后重新输入'
            else:
                user = User(email=email,wechatid=wechatid,password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功，则跳转到登录页面
                return redirect(url_for('login'))

@app.route('/login/', methods=['GET','POST'])
def login():
    """登录页面"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter(User.email == email,User.password == password).first()
        if user:
            session['user_id'] = user.user_id
            # 如果想在31天内都不需要登录
            session.permanent = True
            print(url_for('index'))
            return redirect(url_for('index'))
        else:
            return u'邮箱或者密码错误，请确认后重新登录'

@app.route('/logout')
def logout():
    #删除session中的user_id来实现注销
    #session.pop('user_id')
    session.clear()
    return redirect(url_for('login'))

@app.route('/material_edit', methods=['GET','POST'])
def material_edit():
    if request.method == 'GET':
        mater_id = request.args.get('mater_id')
        if mater_id:
            # return session['user_id']
            material = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id']).first()
            # return str(Material.query.filter(Material.mater_id==mater_id,Material.user_id==session['user_id']))
            return render_template('material_edit.html', material=material)
        else:
            return render_template('material_edit.html')
    else:
        mater_id = request.form['mater_id']
        tag = request.form['tag']
        content = request.form['content']
        edit_time = datetime.utcnow()
        user_id = session['user_id']
        # print(mater_id,tag,content,edit_time,user_id)
        if mater_id:
            material = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id'])
            material.tag = tag
            material.content = content
            material.edit_time = edit_time
            db.session.commit()
        else:
            material = Material(tag=tag,content=content,user_id=user_id,edit_time=edit_time)
            db.session.add(material)
            db.session.commit()

        # return u"提交成功"
        return redirect(url_for('material_list'))

@app.route('/material_list', methods=['GET'])
def material_list():
    mater_id = request.args.get("mater_id")
    tag = request.args.get("tag")
    # 标签唯一问题
    tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])
    # return str(tag_all)
    if mater_id:
        materials = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
        return render_template("material_list.html",materials=materials,tags=tag_all)
    elif tag:
        materials = Material.query.filter(Material.tag==tag,Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
        return render_template("material_list.html",materials=materials,tags=tag_all)
    else:
        materials = Material.query.filter(Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
        return render_template("material_list.html",materials=materials,tags=tag_all)


@app.route('/article_edit', methods=['GET','POST'])
def article_edit():
    if request.method == 'GET':
        artic_id = request.args.get('artic_id')
        tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])
        if artic_id:
            article = Article.query.filter(Article.mater_id==int(artic_id),Article.user_id==session['user_id']).first()
            # return str(Material.query.filter(Material.mater_id==mater_id,Material.user_id==session['user_id']))
            return render_template('article_edit.html', article=article,tags=tag_all)
        else:
            return render_template('article_edit.html',tags=tag_all)
    else:
        artic_id = request.form['artic_id']
        title = request.form['title']
        content = request.form['content']
        edit_time = datetime.utcnow()
        user_id = session['user_id']
        # print(mater_id,title,content,edit_time,user_id)
        if artic_id:
            article = Article.query.filter(Article.mater_id==int(artic_id),Article.user_id==session['user_id'])
            article.title = title
            article.content = content
            article.edit_time = edit_time
            db.session.commit()
        else:
            article = Article(title=title,content=content,user_id=user_id,edit_time=edit_time)
            db.session.add(article)
            db.session.commit()

        # return u"提交成功"
        return redirect(url_for('article_list'))

@app.route('/article_list', methods=['GET'])
def article_list():
    artic_id = request.args.get("artic_id")
    title = request.args.get("title")
    tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])

    if artic_id:
        articles = Article.query.filter(Article.artic_id==int(artic_id),Article.user_id==session['user_id']).order_by(desc(Article.edit_time))
        return render_template("article_list.html",articles=articles,tags=tag_all)
    elif title:
        articles = Article.query.filter(Article.title==title,Article.user_id==session['user_id']).order_by(desc(Article.edit_time))
        return render_template("article_list.html",articles=articles,tags=tag_all)
    else:
        articles = Article.query.filter(Article.user_id==session['user_id']).order_by(desc(Article.edit_time))
        return render_template("article_list.html",articles=articles,tags=tag_all)

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/wx', methods=['GET','POST'])
def wx():
    if request.method == 'GET':
        valicate_params = request.args
        return valication(valicate_params)
    else:
        xml_recv = ET.fromstring(request.data)
        xml_reply = reply_text(xml_recv)
        response = make_response(xml_reply)
        response.content_type = 'application/xml'
        return response
