import os
from flask import Flask, render_template, session, redirect, url_for, flash,request, g
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
app.config['JSON_AS_ASCII'] = False
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
        return "%r*%r*%r*%r" % (self.activity, self.hphoto, self.describe, self.file_wjj)

class Potx(db.Model):
    #用于保存照片的模型
    __tablename__ = 'potxs'
    #设置id表头
    id = db.Column(db.Integer, primary_key = True)
    photoname = db.Column(db.String(64), index=True)
    describe = db.Column(db.Text)
    #设定外键（有可能这个注释是错误的）
    act_id = db.Column(db.Integer, db.ForeignKey('acts.id'))
    #返回函数
    def __repr__(self):
        return "%r*%r" % (self.photoname, self.describe)

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


@app.route('/login/', methods=['GET', 'POST'])
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


@app.route('/logout/')
def logout():
    logout_user()
    flash('You have been logged out.') 
    return redirect("/")


@app.route('/photo')
@login_required
def photo():
    #活动目录界面函数
    cs_list = Act.query.all()

    z_list = []

    for x in cs_list:

        a = str(x)
        b = a.split("*")
        wcl_list = []

        for y in b :
            c = y.strip('\'')

            wcl_list.append(c)

        z_list.append(wcl_list)

    jsjs = 0
    for x in z_list:

        lj = "/static/img/" + x[3] + "/" + x[1]
        z_list[jsjs][1] = lj
        jsjs += 1


    return render_template('photo.html',plist = z_list)


@app.route('/act/<v>')
@login_required
def photoson(v):
    a = Act.query.filter_by(file_wjj=v).first()
    b = Potx.query.filter_by(role=a).all()

    z_list = []

    for x in b:

        a = str(x)
        b = a.split("*")
        wcl_list = []

        for y in b :
            c = y.strip('\'')

            wcl_list.append(c)

        z_list.append(wcl_list)

    jsjs = 0
    for x in z_list:

        lj = "/static/img/" + v + "/" + x[0]
        z_list[jsjs][0] = lj
        jsjs += 1

    return render_template('photoson.html',lista = z_list)



@app.route("/api/upload/",methods=['POST','GET'])
def upjpg():

    lj = request.form["lj"]
    upload_file = request.files['file']
    
    old_file_name = upload_file.filename
    if upload_file:
        file_path = os.path.join("/Users/lucy/Desktop/hlby_web/app/static/img/" + lj, old_file_name)
        upload_file.save(file_path)
        
        return '发送完成'
    else:
        return '发送失败'
    


@app.route('/api/',methods=['POST','GET'])
def apidk():
    text=request.args.get('config')
    if text is not None:
        a = str(text)
        d = a.strip("\"")
        b = d.split("*")
        actname = b[0]
        actms = b[1]
        actfile = b[2]
        photonamew = b[3]

        sss = photonamew.split("!")

        aa = Act(activity=actname,describe=actms,file_wjj=actfile,hphoto=photonamew[0])

        db.session.add(aa)
        js = 0
        for x in sss:
            js += 1

            exec(f"a{js} = Potx(photoname=\"{x}\",describe=\"无描述\",role=aa)")

            exec(f"db.session.add(a{js})")
        
        db.session.commit()

        os.makedirs("/Users/lucy/Desktop/hlby_web/app/static/img/" + b[2])

    return photonamew

if __name__ == '__main__':
    app.run(debug = True)

