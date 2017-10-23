import hashlib
from datetime import datetime
from models import User,Material
import re
import time
from config import WX_TOKEN
from app import db
from sqlalchemy import desc


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
    # print(content)
    # 此处wechatid有待修改为微信号
    user = User.query.filter(User.openid == fromUserName).first()
    if user==None:
        user_re = re.compile(f"邮箱:(?P<email>.+)\n微信号:(?P<wechatid>.+)\n密码:(?P<password>.+)", re.DOTALL)
        user_match = user_re.match(content)
        if user_match == None:
            reply_content = '您尚未注册微信端功能\n\n请发送如下格式的信息注册微信端功能：\n邮箱:(邮箱)\n微信号:(微信号)\n密码:(密码)\n（实际发送信息时请去掉括号，若先前在web端注册过，信息将会被重置）'
            return reply_patten(fromUserName,toUserName,reply_content)
        else:
            regist_wx(user_match.group('email'),user_match.group('wechatid'),user_match.group('password'),fromUserName)
            reply_content = '微信端功能开通成功！注册信息已更新！'
            return reply_patten(fromUserName,toUserName,reply_content)

    if content=="帮助":
        reply_content = "帮助信息\n\n1.微信端功能需要注册方可使用\n2.输入“帮助”可查看帮助信息\n3.输入“历史”可以查看最近保存的一条素材\n4.保存素材信息格式：#标签#内容\n5.所有用作格式识别的标点符号均为英文标点"
    elif content=="历史":
        #此处有待增加内容
        material_last = Material.query.filter(Material.user_id==user.user_id).order_by(desc(Material.edit_time)).first()
        reply_content = f"#{material_last.tag}#{material_last.content}"
    else:
        print(content)
        tag_re = re.compile(f"#(?P<tag>.+)#", re.DOTALL)
        tag_match = tag_re.match(content)

        if tag_match == None:
            tag = '无标签'
        else:
            tag = tag_match.group('tag')
            content = content.replace(tag_match.group(0),'')

        user_id = user.user_id
        edit_time = datetime.utcnow()

        new_material = Material(content=content, user_id=user_id, tag=tag, edit_time=edit_time)
        db.session.add(new_material)
        db.session.commit()

        reply_content = "素材保存成功"

    xlm_reply = reply_patten(fromUserName,toUserName,reply_content)
    # print(xlm_reply)

    return xlm_reply

def regist_wx(email,wechatid,password,openid):
    """注册用户openid"""
    user = User.query.filter(User.email == email).first()
    if user:
        user.openid = openid
        user.password = password
        user.wechatid = wechatid
        db.session.commit()
    else:
        user = User(email=email,wechatid=wechatid,password=password,openid=openid)
        db.session.add(user)
        db.session.commit()
    return

def reply_patten(toUserName,fromUserName,reply_content):
    xlm_reply = f"""<xml>
<ToUserName><![CDATA[{toUserName}]]></ToUserName>
<FromUserName><![CDATA[{fromUserName}]]></FromUserName>
<CreateTime>{str(int(time.time()))}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{reply_content}]]></Content>
</xml>"""
    return xlm_reply
