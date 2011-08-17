from permits import *
from permits.models import *
from permits.parsing import *

@app.route('/')
def index():
	return render_template('upload.html')
	
@app.route('/permit')
def view_permit():
	#find permit by app #
	#display below
	return "view permit"
	
@app.route('/address')
def view_address():
	#find address from url
	#display addres
	return "view address"

@app.route('/upload', methods=['GET','POST'])
def upload_spreadsheet():
	if request.method == 'POST' and 'spreadsheet' in request.files:
		f = request.files['spreadsheet']
		filename = secure_filename(f.filename)
		if filename != '':
			f.save(UPLOAD_PATH + filename)
			flash("Parsing "+ filename)
			parse_csv(UPLOAD_PATH + filename)
	return render_template('upload.html')