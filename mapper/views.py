from flask import Blueprint, request, session, g, redirect, url_for, \
	abort, render_template, flash

mapper_app = Blueprint('mapper_app', __name__,template_folder='templates')

@mapper_app.route('/')
def index():
	return render_template('map.html')