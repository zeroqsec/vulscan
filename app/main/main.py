import re
from flask import Blueprint,request


from app.common.msg import MSG
from app.services.login import User,getCookie
from app.common.encrypt import decrypt
from log.log import getLogger
from cores.colors import  red, white, bad, info,run,que,good
from config.config import key,iv

logger = getLogger(__name__)
app_bp = Blueprint('app_bp',__name__,url_prefix='/app')



@app_bp.route('/')
def hello_word():
    return "Hello World"


@app_bp.route('/login')
def login():
    try:
        # username = request.form['username']
        # password = request.form['password']

        username = request.args.get("username")
        password = request.args.get("password")

        if len(username.replace(" ","")) == 0 \
            or len(password.replace(" ","")) == 0:
            return MSG.Failed(msg="用户名或密码不能为空")
        resp = User.login(username,password)
        if resp is not None:
            return resp
        else:
            return MSG.Failed()
    except Exception as e:
        logger.error("%s {}".format(e) % bad)
        return MSG.Failed()

@app_bp.route('/logout')
def logout():
    try:
        c = getCookie()
        decryptData = str(decrypt(key,iv,bytes(c,encoding='utf-8')))
        decryptData = re.findall(r"b'(.+)'",decryptData)[0]
        resp = User.logout(decryptData)
        if resp is not None:
            return resp
        else:
            return MSG.Failed()
    except Exception as e:
        logger.error("%s {}".format(e) % bad)
        return MSG.Failed()

