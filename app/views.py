from flask import Flask,render_template,redirect,url_for,session,request,make_response,send_from_directory
import xml.etree.ElementTree as ET
import config
from models import User,Material,Article
from app import db,app
from app.wx import valication, reply_text, reply_event, reply_else
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.sql import text
import re


@app.route('/')
def about():
    """首页"""
    return render_template('about.html')

@app.route('/regist', methods=['GET','POST'])
def regist():
    """注册页面"""
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form['email']
        wechatid = request.form['wechatid']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if email=="" or wechatid=="" or password1=="" or password2=="":
            return u"注册信息不能为空"
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

@app.route('/login', methods=['GET','POST'])
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

            return redirect(url_for('about'))
        else:
            return u'邮箱或者密码错误，请确认后重新登录'

@app.route('/logout')
def logout():
    #删除session中的user_id来实现注销
    #session.pop('user_id')
    session.clear()
    return redirect(url_for('login'))

@app.route("/get_material",methods=['GET','POST'])
def get_material():
    """用于查询标签"""
    if request.method == "GET":
        key = request.args.get('key')
        tag = request.args.get('tag')
    else:
        key = request.form['key']
        tag = request.form['tag']
    print(key,tag)
    if key:
        materials = Material.query.filter(Material.content.like(f"%{key}%"),Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
    elif tag:
        materials = Material.query.filter(Material.tag.like(f"%{tag}%"),Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
    else:
        materials = Material.query.filter(Material.user_id==session['user_id']).order_by(desc(Material.edit_time))
    # print(materials)
    return render_template('get_material.html',materials=materials)

@app.route('/material', methods=['GET'])
def material():
    mater_id = request.args.get('mater_id')
    if mater_id:
        # return session['user_id']
        material = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id']).first()
        # return str(Material.query.filter(Material.mater_id==mater_id,Material.user_id==session['user_id']))
        return render_template('material.html', material=material)
    else:
        return render_template('material_.html')

@app.route('/material_edit', methods=['GET','POST'])
def material_edit():
    if request.method == 'GET':
        mater_id = request.args.get('mater_id')
        if mater_id:
            material = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id']).first()
            return render_template('material_edit.html', material=material)
        else:
            return render_template('material_edit.html')
    else:
        mater_id = request.form['mater_id']
        content = request.form['content']

        tag_re = re.compile(f"#(?P<tag>.+)#", re.DOTALL)
        tag_match = tag_re.match(content)

        if tag_match == None:
            tag = '无标签'
        else:
            tag = tag_match.group('tag')
            content = content.replace(tag_match.group(0),'')

        edit_time = datetime.utcnow()
        user_id = session['user_id']
        # print(mater_id,tag,content,edit_time,user_id)
        if mater_id:
            material = Material.query.filter(Material.mater_id==int(mater_id),Material.user_id==session['user_id']).first()
            material.tag = tag
            material.content = content
            material.edit_time = edit_time
            db.session.add(material)
            db.session.commit()
        else:
            material = Material(tag=tag,content=content,user_id=user_id,edit_time=edit_time)
            db.session.add(material)
            db.session.commit()

        return redirect(url_for('index'))

@app.route('/article', methods=['GET'])
def article():
    artic_id = request.args.get('artic_id')
    tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])
    if artic_id:
        article = Article.query.filter(Article.artic_id==int(artic_id),Article.user_id==session['user_id']).first()
        # return str(Material.query.filter(Material.mater_id==mater_id,Material.user_id==session['user_id']))
        return render_template('article.html', article=article,tags=tag_all)
    else:
        return render_template('article_edit.html',tags=tag_all)


@app.route('/article_edit', methods=['GET','POST'])
def article_edit():
    if request.method == 'GET':
        artic_id = request.args.get('artic_id')
        tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])
        if artic_id:
            article = Article.query.filter(Article.artic_id==int(artic_id),Article.user_id==session['user_id']).first()
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
            article = Article.query.filter(Article.artic_id==int(artic_id),Article.user_id==session['user_id']).first()
            article.title = title
            article.content = content
            article.edit_time = edit_time
            db.session.add(article)
            db.session.commit()
        else:
            article = Article(title=title,content=content,user_id=user_id,edit_time=edit_time)
            db.session.add(article)
            db.session.commit()

        # return u"提交成功"
        return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
def index():
    tag = request.args.get("tag")
    key = request.args.get("key")
    try:
        page = int(request.args.get("page"))
    except:
        page = 1
    tag_all = Material.query.with_entities(Material.tag.distinct().label("tag")).filter(Material.user_id==session['user_id'])

    if tag:
        sql = text("select id,title,tag,content,user_id,edit_time,type  from all_draft where user_id = :user_id_1 and (tag like concat('%',:tag_1,'%'))  order by edit_time desc")
        result = db.engine.execute(sql,user_id_1=session['user_id'],tag_1=tag)
        return render_template("index.html",items=result,tags=tag_all)
    elif key:
        sql = text("select id,title,tag,content,user_id,edit_time,type  from all_draft   where user_id = :user_id_1 and (title like concat('%',:key_1,'%') or content like concat('%',:key_1,'%')) order by edit_time desc")
        result = db.engine.execute(sql,user_id_1=session['user_id'],key_1=key)
        return render_template("index.html",items=result,tags=tag_all)
    else:
        sql = text("select id,title,tag,content,user_id,edit_time,type  from all_draft where user_id = :user_id_1 order by edit_time desc")
        result = db.engine.execute(sql,user_id_1=session['user_id'])
        return render_template("index.html",items=result,tags=tag_all)


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
        msgtype = xml_recv.find("MsgType").text
        # print(request.data)
        if msgtype == "event":
            xml_reply = reply_event(xml_recv)
        elif msgtype == "text":
            xml_reply = reply_text(xml_recv)
        else:
            xml_reply = reply_else(xml_recv)
        response = make_response(xml_reply)
        response.content_type = 'application/xml'
        return response
