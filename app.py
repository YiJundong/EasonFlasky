#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class Role(db.Model):
    '''
    举例创建新角色：
    admin_role = Role(name='admin')
    user_role = Role(name='user')
    '''

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    #unique表示角色名不能重复
    name = db.Column(db.String(64), unique=True)
    #backref参数向User模型中临时添加一个role属性，这一属性可替代role_id访问Role模型
    #lazy:指定如何加载相关记录，dynamic表示不加载记录，但提供加载记录的查询
    users = db.relationship('User', backref='role', lazy='dynamic')

    #返回一个具有可读性的字符串表示模型(model),可在调试和测试时使用，没弄懂
    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    '''
    举例创建新用户：
    user_eason=User(username='eason',role=admin_role)
    user_tom=User(username='tom',role=user_role)
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    #当外键只有一个时，优先使用外键
    #当外键多于一个时，就要为Role中的db.relationship提供额外参数，从而确定外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    db.create_all()
    #manager.run()
    app.run()
