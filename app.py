from flask import Flask,render_template,redirect, url_for, session,request
import xml.etree.ElementTree as ET


app = Flask(__name__)

@app.route('/', methods=['GET'])
def login_page():
    """访问根目录，显示登录页面"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_operate():
    """邮箱登录验证功能"""
    # email =
    # pasword =

    # login_state = verifi_user(email,pasword)
    if login_state:
        session['username'] = email
        # 重定向
        redirect(url_for('index'))
    else:
        return '邮箱或密码不正确'

@app.route('/login_by_weixin', methods=['POST'])
def login_by_weixin():
    """微信登录验证功能（假想）"""
    weixin_id =
    user = get_user_by_weixinid(weixin_id)
    if user['email'] == None:
        redirect(url_for('user_input'))
    else:
        session['username'] = email
        # 重定向
        redirect(url_for('index'))

@app.route('/user_input', methods=['POST'])
def update_user_data():
    """完善用户数据操作"""
    email =
    password =
    update_user(email,password)


@app.route('/material', methods=['GET','POST'])
def material_page():
    """素材列表页面"""

    return render_template('material_list.html', tag_list=tag_list, material_list= material_list)

@app.route('/material/<material_num>', methods=['GET','POST'])
def material_edit(material_num):
    """素材编辑页面"""
    naterial = get_magerial(material_num)
    content = request.form('')

    return render_template('material_edit.html', tag_list=tag_list, material_list= material_list)


@app.route('/atricle', methods=['GET','POST'])
def atricle_page():
    """文章列表页面"""

    return render_template('atricle_list.html', tag_list=tag_list, atricle_list= atricle_list)

@app.route('/atricle/<article_num>', methods=['GET','POST'])
def atricle_edit(article_num):
    """文章编辑页面"""
    title = request.form('')
    content = request.form('')

    article = get_article(article_num)


    tag_list = get_tag_list()
    material_list = get_magerial_list()

    return render_template('article_edit.html', tag_list=tag_list, material_list= material_list, title =title,content=content)

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
