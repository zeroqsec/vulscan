from flask import Flask


def create_app():
    app = Flask(__name__)

    # 注册蓝图
    from app.main.main import app_bp
    app.register_blueprint(app_bp)

    return app