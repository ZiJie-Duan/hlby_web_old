import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required
from flask_login import logout_user, login_user

#初始化登陆
login_manager = LoginManager()
#初始化路径
basedir = os.path.abspath(os.path.dirname(__file__))
#初始化app
app = Flask(__name__)
#初始化数据库设置
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#初始化登陆安全配置
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
app.config['SECRET_KEY']='23432434ghj'
#初始化 
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)



		   #导入登陆模块
class Users(UserMixin,db.Model):
    #用于保存用户名以及密码的模型
    __tablename__ = 'users'
    #设置id表头
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    #返回函数
    def __repr__(self):
        return "%r" % self.password

class Act(db.Model):
    #用于保存活动的模型
    __tablename__ = 'acts'
    #设置id表头
    id = db.Column(db.Integer, primary_key = True)
    activity = db.Column(db.String(64), index=True)
    hphoto = db.Column(db.String(64))
    describe = db.Column(db.Text)
    file_wjj = db.Column(db.String(64))
    #设定返回
    photx = db.relationship('Potx', backref='role')
    #返回函数
    def __repr__(self):
        return "%r*%r*%r" % (self.activity, self.hphoto, self.describe)

class Potx(db.Model):
    #用于保存照片的模型
    __tablename__ = 'potxs'
    #设置id表头
    id = db.Column(db.Integer, primary_key = True)
    photoname = db.Column(db.String(64), unique=True, index=True)
    describe = db.Column(db.Text)
    #设定外键（有可能这个注释是错误的）
    act_id = db.Column(db.Integer, db.ForeignKey('acts.id'))
    #返回函数
    def __repr__(self):
        return "%r*%r" % (self.photoname, self.describe)

db.create_all()

a = Users(username = "guest",password = "asdfgh123456")
b = Users(username = "sosomu",password = "123456")
c = Act(activity = "第一次校会",hphoto="1.jpg",file_wjj = "a",describe="这是我们第一次校会哈哈哈哈哈")
d = Potx(photoname = "2.jpg",describe="这也不知道是啥",role = c)
e = Potx(photoname = "3.jpg",describe="这也不知道是啥",role = c)
f = Potx(photoname = "4.jpg",describe="这也不知道是啥",role = c)
db.session.add_all([a,b,c,d,e,f])
db.session.commit()


act_list = Act.query.get(1)
aa = act_list[0]
ab = str(aa)
ac = ab.split("*")
zz = []
for x in ac:
    zz.append(x.split("\'"))

print(zz)


