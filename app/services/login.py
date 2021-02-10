from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask import session,make_response,request

from app.common.msg import MSG
from app.common.encrypt import encrypt,decrypt
from log.log import getLogger
from cores.colors import  red, white, bad, info,run,que,good
from config.config import key,iv

logger = getLogger(__name__)
db = SQLAlchemy()

# app = Flask(__name__)
# from flask import Flask,session
# app.secret_key = '!@#$%^&*()11'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1/vulhub'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self,username,password):
        self.username = username
        self.password = password

    @staticmethod
    def login(username,password):
        if len(User.query.filter_by(username = username,password = password).all()) > 0:
            # 创建session
            session[username] = username
            resp = setCookie(username)
            return resp
        return None


    @staticmethod
    def logout(username):
        try:
            session.pop(username)
            resp = delCookie()
            return resp
        except Exception as e:
            logger.error("%s {}".format(e) %bad)
            return None


    @staticmethod
    def add(username,password):
        user = User(username,password)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def delete(username):
        User.query.filter_by(username = username).delete()

    @staticmethod
    def modify(username,password):
        if len(password.replace(" ","")) == 0:
            User.query.filter_by(username = username).update({'username':username})
        else:
            User.query.filter_by(username = username).update({'username':username,'password':password})

class Auth:
    __tablename__ = "Auth"
    auth_id = db.Column(db.Integer, primary_key=True)
    decription = db.Column(db.String(255), unique=True)

    def __init__(self,auth_id,decription):
        self.auth_id = auth_id
        self.decription = decription


class AuthControl:
    __tablename__ = "AuthControl"
    id = db.Column(db.Integer)
    auth_id = db.Column(db.Integer)

    def __init__(self,id,auth_id):
        self.id = id
        self.auth_id = auth_id


# 设置cookie
def setCookie(username):
    try:
        encryptData = encrypt(bytes(username,encoding='utf-8'),key,iv)
        resp = make_response(MSG.Success(msg="success"))
        encryptData = str(encryptData,encoding='utf-8')
        resp.set_cookie('id',encryptData,max_age = 3600)
        return resp
    except TypeError:
        logger.error("%s encrypt string argument without an encoding." %bad)
    except Exception as e:
        logger.error("%s {}".format(e) %bad)


# 删除cookie
def delCookie():
    resp = make_response(MSG.Success())
    resp.delete_cookie('id')
    return resp

# 获取cookie
def getCookie():
    c = request.cookies.get("id")
    return c

def userIsExist(f):
    '''
    judge user is existing
    '''
    @wraps(f)
    def decorated(username,*args):
        if type(len(User.query.filter_by(username=username).all())) == 0:
            return MSG.Failed(msg="用户不存在")
        else:
            return f(username,*args)
    return decorated

def allArgsIsNotNull(f):
    '''
    judge all args is not null
    '''
    @wraps(f)
    def decorated(*args):
        for arg in args:
            if len(arg.replace(" ","")) == 0:
               return MSG.Failed(msg="参数不能为空")
        return f(*args)
    return decorated

def authorization():
    def authorization_decorated(f):
        @wraps(f)
        def wrapped_function(username):
            if username not in session:
                return MSG.Failed()
            else:
                return f()
        return wrapped_function
    return authorization_decorated




