#-*- coding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

'''
看了flask-mail的文档，以及十几篇相关博客，注册时还是无法收到确认邮件，
遂放弃邮件确认功能，直接在shell中注册新用户。

修改密码以及修改邮箱功能，也无法实现，因为收不到确认邮件。
但是我单独写的send_mail.py运行正常，不知为何。代码见我个人博客。

用户可以直接在shell中注册，如下：
python manage.py db upgrade
python manage.py shell
>>>u=User(email='john@example.com',username='john',password='cat',confirmed=True)
>>>db.session.add(u)
>>>db.session.commit()
#ctrl+Z退出shell
python manage.py runserver --host 0.0.0.0
'''
#163作为发件箱的相关配置，假设邮箱为whattheheck@163.com,密码为123456
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL= True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'whattheheck'
    MAIL_PASSWORD = '123456'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'whattheheck@163.com'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
