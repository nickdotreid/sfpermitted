from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash
from flaskext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

