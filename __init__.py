from flask import Flask,request,url_for,render_template,abort,redirect,flash,session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ankit:ankitgohel@localhost/appstore"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True 
app.secret_key='ihnedsvhfdol'
db=SQLAlchemy(app)

admin = Admin(app, name='The App Store', template_mode='bootstrap3')

class Apps(db.Model):
	app_id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	thumbnail = db.Column(db.String(100))
	developer = db.Column(db.String(100))

	def __init__(self,name='', thumbnail='', developer=''):
		self.name = name
		self.thumbnail = thumbnail
		self.developer = developer

class AppsAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['name','thumbnail','developer']

class Details(db.Model):
	details_id = db.Column(db.Integer, primary_key = True)
	app_id = db.Column(db.Integer)
	screenshot = db.Column(db.String(100))
	description = db.Column(db.String(1000))
	version = db.Column(db.String(100))
	price = db.Column(db.String(100))

	def __init__(self,app_id=None,screenshot='',description='',version='',price=None):
		self.app_id = app_id
		self.screenshot = screenshot
		self.description = description
		self.version = version
		self.price = price

class DetailsAdmin(sqla.ModelView):
	column_display_pk = True
	form_columns = ['app_id','screenshot','description','version','price']

db.create_all()

admin.add_view(AppsAdmin(Apps, db.session))
admin.add_view(DetailsAdmin(Details, db.session))

@app.route('/')
def home():
	all_apps = Apps.query.all()
	return render_template('index.html',all_apps = all_apps)

@app.route('/apps')
def show():
	all_apps = Apps.query.all()
	return render_template('apps.html',all_apps = all_apps)

@app.route('/apps/<id>')
def showapp(id):
	currentapp = Apps.query.filter_by(app_id = id).first()
	app_details = Details.query.filter_by(app_id = id).first()
	return render_template('appdisplay.html',app = currentapp, app_details = app_details)

if __name__=='__main__':
	app.run()