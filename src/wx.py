import hashlib
import time
from models import User,Material
import re
from config import WX_TOKEN

def valication(params):
    token = WX_TOKEN
    signature = params.get('signature')
    timestamp = params.get('timestamp')
    nonce = params.get('nonce')
    echostr = params.get('echostr')
    # print(signature, timestamp, nonce, echostr)

    if timestamp == None or nonce == None or echostr == None:
        return ""
    else:
        arglist = [token, timestamp, nonce]
        arglist.sort(key=str.lower)
        sha1 = hashlib.sha1()
        sha1.update("".join(arglist).encode('utf-8'))
        hashcode = sha1.hexdigest()
        #print("handle/GET func: hashcode, signature: ", hashcode,",", signature)
        if hashcode == signature:
            # print(echostr)
            return echostr
        else:
            return ""

def reply_text(xml_recv):
    """回复函数，"""
    toUserName = xml_recv.find("ToUserName").text
    fromUserName = xml_recv.find("FromUserName").text
    content = xml_recv.find("Content").text
    msgtype = xml_recv.find("MsgType").text

    # 此处wechatid有待修改为微信号
    user = User.query.filter(wechatid==fromUserName).first()
    # if user==None:
    #     user = regist_wx(fromUserName)

    if content=="历史":
        #此处有待增加内容
        material_last = Material.query.filter(user_id=user.user_id).first()
        reply_text = material_last.content

    else:
        tag_re = re.match(f"#(?P<tag>.+)#", re.DOTALL)
        tag_match = tag_re.match(content)
        tag = tag_match.group('tag')
        if tag == None:
            tag = '无标签'
        else:
            content = content.replace(tag_match.group(0),'').trip()

        user_id = user.user_id
        edit_time = time.time()

        new_material = Material(content, user_id, tag, edit_time)
        db.session.add(new_material)
        db.session.commit()

        reply_content = "素材保存成功"

    xlm_reply = f"""<xml>
<ToUserName><![CDATA[{fromUserName}]]></ToUserName>
<FromUserName><![CDATA[{toUserName}]]></FromUserName>
<CreateTime>{str(int(time.time()))}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{reply_content}]]></Content>
</xml>"""

    return xlm_reply

def regist_wx(fromUserName):
    """注册邮箱、密码为空的用户"""
    user = User(,,,fromUserName)
    db.session.add(user)
    db.session.commit
    return user
