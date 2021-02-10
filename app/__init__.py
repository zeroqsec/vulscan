from flask import Flask
from config.config import SQLALCHEMY_DATABASE_URI

def create_app():
    app = Flask(__name__)

    # 注册蓝图
    from app.main.main import app_bp
    app.register_blueprint(app_bp)

    # 数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # session
    app.secret_key = '!@#$%^&*()11'
    from app.services.login import db
    db.init_app(app)

    return app