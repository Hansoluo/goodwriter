#encoding:utf-8

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app
from app import db
from models import User


# 模型 -> 迁移文件 -> 表
# init初始化迁移环境
# migrate将模型生成迁移文件
# upgrade真正将表映射到表中
#
# manager = Manager(app)
#
# # 1.使用flask_migrate，必须绑定app和db
# migrate = Migrate(app,db)
#
# # 2.把MigrateCommand命令添加到manager中
# manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    app.run(debug=True)
