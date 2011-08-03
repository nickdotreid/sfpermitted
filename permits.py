from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from flaskext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Permit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	app_id = db.Column(db.String(80), unique=True)
	file_date = db.Column(db.Integer)
	status_date = db.Column(db.Integer)
	expiration_date = db.Column(db.Integer)
	issued = db.Column(db.Boolean)
	
	address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
	address = db.relationship('Address', backref=db.backref('permits', lazy='dynamic'))
	
	def __init__(self, app_id, file_date, status_date, expiration_date, issued):
		self.app_id = app_id
		self.file_date = file_date
		self.status_date = status_date
		self.expiration_date = expiration_date
		self.issued = issued
		
		
	def __repr__(self):
		return '<Permit %r>' % self.app_id
		

class Address(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	street = db.Column(db.String(500))
	
	def __init__(self,street):
		self.street = street
		
	def __repr__(self):
		return '<Address %r>' % self.street
