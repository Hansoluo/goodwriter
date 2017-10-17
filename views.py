from flask import Flask,render_template,redirect,url_for,session,request
import xml.etree.ElementTree as ET
import config
from models import User
from exts import db
import re

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

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
        email = request.form.get('email')
        wechatid = request.form.get('wechatid')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

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
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email,User.password == password).first()
        if user:
            session['user_id'] = user.user_id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'邮箱或者密码错误，请确认后重新登录'

@app.route('/logout/')
def logout():
    #删除session中的user_id来实现注销
    #session.pop('user_id')
    session.clear()
    return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.user_id == user_id).first()
        if user:
            return {'user':user}
    return {}


@app.route('/main', methods=['GET','POST'])
def main():
    """主页面，查询用户数据渲染页面，按钮跳转页面"""
    if 'new_draft' in request.form.keys():
        return render_template('new_draft.html')
    elif 'edit_draft' in request.form.keys():
        return render_template('edit_draft.html', db.Text = db.Text)
    else:
        drafts = Draft.query.filter_by(author_id=current_user._get_current_object()).all()
        tag_list = Counter(draft.tag).most_common()
        page = request.args.get('page', 1, type=int)
        pagination = Draft.query.order_by(Draft.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        drafts = pagination.items
        return render_template('index.html', drafts=drafts, tag_list=tag_list
                               pagination=pagination)


@app.route('/drafts', methods=['GET','POST'])
def drafts():
    """写素材页面，写完保存到数据库
       回到主页面按钮和开新页面按钮"""
    form = DraftForm()
    if form.validate_on_submit():
        tag = tag_extract(form.body.data)
        draft = Draft(body=form.body.data,
                      author_id=current_user._get_current_object(),
                      tag=tag)
        db.session.add(draft)
        db.session.commit()
        return redirect(url_for('drafts'))
    if 'home' in request.form.keys():
        return redirect(url_for('main'))
    if 'new_draft' in request.form.keys():
        return redirect(url_for('drafts'))

def tag_extract(draft):
    """从素材中提取多个标签，有则返回第一个标签，无则返回<未标注>"""
    tag1 = re.findall(r"#[\u4e00-\u9fa5\\w]+#", draft)
    a = []
    if tag1:
        for i in tag1:
            tag2 = re.sub(r'\W', '', i)
            a.append(tag2)
    else:
         a.append("未标注")

    return a[0]

@app.route('/wx', methods=['GET','POST'])
def wx():
    if request.method == 'GET':
        valicate_params = request.args
        return valication(valicate_params)
    else:
        xml_recv = ET.fromstring(request.data)
        xml_reply = reply_text(path, xml_recv)
        response = make_response(xml_reply)
        response.content_type = 'application/xml'
        return response
