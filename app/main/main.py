from flask import Blueprint


app_bp = Blueprint('app_bp',__name__,url_prefix='/app')

@app_bp.route('/')
def hello_word():
    return 'hello world!'


