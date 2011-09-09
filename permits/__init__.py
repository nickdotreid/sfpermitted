from flask import Flask
from werkzeug import secure_filename
from flaskext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
db = SQLAlchemy(app)

UPLOAD_PATH = 'data_raw/'