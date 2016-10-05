#-*- coding:utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
import sys, logging

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

'''
初始化flask_login.
LoginManager的对象的session_protection属性可以设为None,
basic或strong。当为strong时，flask-login会记录客户端的ip地址和浏览器的
用户代理信息，如果发现异常就登出用户。
login_view属性设置登录页面的端点，此处登录路由在蓝本中定义，所以要在login
前面加上蓝本的名字。
'''
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

#工厂函数
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    #可在heroku log输出错误信息
    #app.logger.addHandler(logging.StreamHandler(sys.stdout))
    #app.logger.setLevel(logging.ERROR)

    return app


