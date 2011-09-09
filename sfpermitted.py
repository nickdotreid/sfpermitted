from flask import Flask
from permits.views import permit_app

app = Flask(__name__)
#app.config.from_object('sfpermitted.settings') #not sure where this should come from
app.config.from_envvar('YOURAPPLICATION_SETTINGS')

app.register_blueprint(permit_app,url_prefix='/permits')