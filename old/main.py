import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
#from mods import paswd


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'haileytianjinlucycore'


#定义服务器模型

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	users = db.relationship('Pas', backref='username')
	password = db.Column(db.String(64), unique=True)
	
	def __repr__(self):
		return '%r' % self.username


class Pas(db.Model):
	__tablename__ = 'passwords'
	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(64), unique=True, index=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __repr__(self):
		return '%r' % self.password

#=======================

class Act(db.Model):
	__tablename__ = 'activity'
	id = db.Column(db.Integer, primary_key=True)
	activity = db.Column(db.String(64), unique=True)
	#图像反向
	photo = db.relationship('Photo', backref='act')

	strs = db.relationship('Describe', backref='act')

	def __repr__(self):
		return '%r' % self.activity

class Photo(db.Model):
	__tablename__ = 'photo'
	id = db.Column(db.Integer, primary_key=True)
	photo_name = db.Column(db.String(64), unique=True, index=True)
	act_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

	def __repr__(self):
		return '%r' % self.photo_name

class Describe(db.Model):
	__tablename__ = 'describe'
	id = db.Column(db.Integer, primary_key=True)
	describe = db.Column(db.String(1024), unique=True, index=True)
	act_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

	def __repr__(self):
		return '%r' % self.describe


'''
with open("test.json") as zx:
	tssss = json.load(zx)
'''
