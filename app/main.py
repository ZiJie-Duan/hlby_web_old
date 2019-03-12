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



#数据库---------模型声明----------

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
    __tablename__ = 'act'
    #设置id表头
    id = db.Column(db.Integer, primary_key = True)
    activity = db.Column(db.String(64), unique=True, index=True)
    describe = db.Column(db.Text)
    #设定返回
    pname = db.relationship('Potx', backref='role')
    #返回函数
    def __repr__(self):
        return "%r" % self.password

class Potx(db.Model):
    #用于保存照片的模型
    __tablename__ = 'photx'
    #设置id表头
    id = db.Column(db.Integer, primary_key = True)
    photoname = db.Column(db.String(64), unique=True, index=True)
    describe = db.Column(db.Text)
    #设定外键（有可能这个注释是错误的）
    act_id = db.Column(db.Integer, db.ForeignKey('act.id'))
    #返回函数
    def __repr__(self):
        return "%r" % self.password

#数据库---------模型声明----------



#表单声明 ----- ----- ----- ----- -----

class NameForm(FlaskForm):
    username = StringField('Please type in your username', validators=[DataRequired()])
    password = PasswordField('Please type in your password', validators=[DataRequired()])
    submit = SubmitField('Submit')

#表单声明 ----- ----- ----- ----- -----



#其他声明 ----- ----- ----- ----- -----

#登陆回调函数
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#其他声明 ----- ----- ----- ----- -----



#url映射 ------ ------- ------- ------- --------

#错误反馈
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#错误反馈
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    ztm = "0"
    #获取表单
    form = NameForm()
    #判断表单是否为空
    if form.validate_on_submit():
        #从数据库获取密码
        userpawd = Users.query.filter_by(username=form.username.data).first()
        #进行密码格式转换
        try:
            userpawd_cl = str(userpawd).strip("\'") 
        except:
            userpawd_cl = "0"
        #判断是否符合要求
        if userpawd is not None:
            if userpawd_cl == form.password.data:
                login_user(userpawd,False)
                #直接转跳入photo页面
                return redirect("photo")
            else:
                flash('Invalid username/password!')
        else:
            flash('Invalid username/password!')
        #返回状态
    return render_template('login.html', form=form, ztm = ztm)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.') 
    return redirect("/")


@app.route('/photo')
@login_required
def photo():
    act_list = Act.query.all()
    
    return render_template('photo.html')

@app.route('/act/<v>')
@login_required
def photoson():
    return render_template('photoson.html')


if __name__ == '__main__':
    app.run(debug = True)

