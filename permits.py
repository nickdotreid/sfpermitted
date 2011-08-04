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

UPLOAD_PATH = '../uploads/'


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
		row = permit_row_clean(row)
		if add_permit(row):
			count+=1
	if count>0:
		flash("Added " + str(count) + "permits")
		
def permit_row_clean(row):
	clean = {}
	for key in row.keys():
		if row[key]:
			if re.search('(APP)',key):
				clean['app_id'] = row[key].lstrip('# ')
			if re.search('FILE',key):
				clean['file_date'] = make_unix_from_string(row[key])
			if re.search('EXPIRATION',key):
				clean['expiration_date'] = make_unix_from_string(row[key])
	return clean

def make_unix_from_string(letters):
	return int(mktime(time.strptime(letters,'%d-%b-%y')))

def add_permit(data):
	# find or make address
#	if Permit.query.filter_by(app_id=data['app_id']).first() is None:
	permit = Permit(data['app_id'],data['file_date'],data['expiration_date'])
	db.session.add(permit)
	db.session.commit()
	return True

class Permit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	app_id = db.Column(db.String(80))
	file_date = db.Column(db.Integer)
	expiration_date = db.Column(db.Integer)

#	address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
#	address = db.relationship('Address', backref=db.backref('permits', lazy='dynamic'))

	def __init__(self, app_id, file_date=0, expiration_date=0):
		self.app_id = app_id
		self.file_date = file_date
		self.expiration_date = expiration_date


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
