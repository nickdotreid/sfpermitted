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

def add_permit(data):
	# find or make address
#	if Permit.query.filter_by(app_id=data['app_id']).first() is None:
	if 'app_id' in data and 'status_date' in data and 'file_date' in data and 'expiration_date' in data and 'street_number' in data and 'street_name' in data and 'street_suffix' in data:
		address = Address(data['street_number'],data['street_name']+" "+data['street_suffix'])
		permit = Permit(data['app_id'],data['file_date'],data['status_date'],data['expiration_date'])
		permit.address = address
		db.session.add(address)
		db.session.add(permit)
		db.session.commit()
		return True
	return False