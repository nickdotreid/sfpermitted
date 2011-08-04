from permits import *
from permits.models import *

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
			if re.search('STATUS_DATE',key):
				clean['status_date'] = make_unix_from_string(row[key])
			if re.search('STREET_NUMBER',key):
				clean['street_number'] = row[key]
			if re.search('AVS_STREET_NAME',key):
				clean['street_name'] = row[key]
			if re.search('AVS_STREET_SFX',key):
				clean['street_suffix'] = row[key]
	return clean

def make_unix_from_string(letters):
	return int(mktime(time.strptime(letters,'%d-%b-%y')))

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