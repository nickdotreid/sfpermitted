from permits import *
from permits.models import *
from permits.parsing import *

@app.route('/')
def index():
	return render_template('upload.html')
	
@app.route('/permit')
def view_permit():
	permits = Permit.query.all()
	return render_template('permits.html', permits=permits, total_permits=len(permits))
	
@app.route('/address')
def view_address():
	addresses = Address.query.all()
	return render_template('addresses.html', addresses=addresses, total_addresses = len(addresses))

@app.route('/upload', methods=['GET','POST'])
def upload_spreadsheet():
	if request.method == 'POST' and 'spreadsheet' in request.files:
		f = request.files['spreadsheet']
		filename = secure_filename(f.filename)
		if filename != '':
			f.save(UPLOAD_PATH + filename)
			flash("Parsing "+ filename)
			rows = parse_csv(UPLOAD_PATH + filename)
			permits_added = 0
			for permit in rows:
				if add_permit(permit):
					permits_added += 1
			if permits_added > 0:
				flash(str(permits_added) + " new permits added")
	return render_template('upload.html')