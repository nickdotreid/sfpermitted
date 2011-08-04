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

import permits.views