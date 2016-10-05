#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
删除了邮件验证功能、修改邮箱、修改密码、重设密码，以及互相关注功能的相关代码

'''
import os
from app import create_app, db
from app.models import User, Role, Permission, Post, Comment, Category, Guestbook
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User,Category=Category, Role=Role,
                Permission=Permission, Post=Post, Comment=Comment, Guestbook=Guestbook)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    #Role.insert_roles()



if __name__ == '__main__':
    manager.run()
