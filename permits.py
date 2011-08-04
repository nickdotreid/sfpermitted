from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from werkzeug import secure_filename
from flaskext.sqlalchemy import SQLAlchemy

import csv
import time
import re
from time import mktime

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

UPLOAD_PATH = '../uploads'


@app.route('/')
def index():
	return render_template('upload.html')

@app.route('/upload', methods=['GET','POST'])
def upload_excel():
	if request.method == 'POST' and 'spreadsheet' in request.files:
		f = request.files['spreadsheet']
		filename = secure_filename(f.filename)
		f.save(UPLOAD_PATH + filename)
		flash("got spreadsheet "+ filename)
		parse_excel(UPLOAD_PATH + filename)
	if request.method == 'POST':
		flash("posted")
	return render_template('upload.html')
	
def parse_excel(file_location):
	data = csv.DictReader(open(file_location))
	count = 0
	for row in data:
		if add_permit(row):
			count+=1
	if count>0:
		flash("Added " + str(count) + "permits")
		
def permit_row_clean(row):
	clean = {}
	#clean keys
	#big giant switch
	for key in row.keys():
		if re.search('(APP)',key):
			clean['app_id'] = row[key]
		if re.search('FILE',key):
			clean['file_date'] = int(mktime(time.strptime(row[key],'%d-%b-%y')))
	return clean

def add_permit(data):
	# if permit ID does not exist
	#permit = Permit(data['APPLICATION #'].strip('# '),)
	return True

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


app.run(debug=True)
