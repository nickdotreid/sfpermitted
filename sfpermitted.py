from flask import Flask
from permits.views import permit_app

app = Flask(__name__)
app.register_blueprint(permit_app,url_prefix='/permits')