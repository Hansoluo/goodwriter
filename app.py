from flask import Flask,render_template,redirect,url_for,session,request
import xml.etree.ElementTree as ET
import config
from models import User
from exts import db

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



# @app.route('/login', methods=['POST'])
# def login_operate():
#     """邮箱登录验证功能"""
#     # email =
#     # pasword =
#
#     # login_state = verifi_user(email,pasword)
#     if login_state:
#         session['username'] = email
#         # 重定向
#         redirect(url_for('index'))
#     else:
#         return '邮箱或密码不正确'

# @app.route('/login_by_weixin', methods=['POST'])
# def login_by_weixin():
#     """微信登录验证功能（假想）"""
#     weixin_id =
#     user = get_user_by_weixinid(weixin_id)
#     if user['email'] == None:
#         redirect(url_for('user_input'))
#     else:
#         session['username'] = email
#         # 重定向
#         redirect(url_for('index'))
#
# @app.route('/user_input', methods=['POST'])
# def update_user_data():
#     """完善用户数据操作"""
#     email =
#     password =
#     update_user(email,password)
#
#
# @app.route('/material', methods=['GET','POST'])
# def material_page():
#     """素材列表页面"""
#
#     return render_template('material_list.html', tag_list=tag_list, material_list= material_list)
#
# @app.route('/material/<material_num>', methods=['GET','POST'])
# def material_edit(material_num):
#     """素材编辑页面"""
#     naterial = get_magerial(material_num)
#     content = request.form('')
#
#     return render_template('material_edit.html', tag_list=tag_list, material_list= material_list)
#
#
# @app.route('/atricle', methods=['GET','POST'])
# def atricle_page():
#     """文章列表页面"""
#
#     return render_template('atricle_list.html', tag_list=tag_list, atricle_list= atricle_list)
#
# @app.route('/atricle/<article_num>', methods=['GET','POST'])
# def atricle_edit(article_num):
#     """文章编辑页面"""
#     title = request.form('')
#     content = request.form('')
#
#     article = get_article(article_num)
#
#
#     tag_list = get_tag_list()
#     material_list = get_magerial_list()
#
#     return render_template('article_edit.html', tag_list=tag_list, material_list= material_list, title =title,content=content)
#
# @app.route('/wx', methods=['GET','POST'])
# def wx():
#     if request.method == 'GET':
#         valicate_params = request.args
#         return valication(valicate_params)
#     else:
#         xml_recv = ET.fromstring(request.data)
#         xml_reply = reply_text(path, xml_recv)
#         response = make_response(xml_reply)
#         response.content_type = 'application/xml'
#         return response


if __name__ == '__main__':
    app.run(debug=True)
