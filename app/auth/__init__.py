#-*- coding:utf-8 -*-
from flask import Blueprint

auth = Blueprint('auth', __name__)

#这行代码搞不懂
from . import views
