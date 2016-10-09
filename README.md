# EasonFlasky
学习《FlaskWeb开发》，做的第一个简易博客。

heroku最终部署版本。

请先进行本地测试，成功后再尝试远程部署。
此版本在win7下CMD中输入以下命令可成功运行：

1.开启虚拟环境

2.python manage.py shell
+ db.create_all()
+ Role.insert_roles()
+ Ctrl+Z

3.heroku local web -f procfile.windows
