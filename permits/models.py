from permits import db

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

class Permit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	app_id = db.Column(db.String(80))
	file_date = db.Column(db.Integer)
	status_date = db.Column(db.Integer)
	expiration_date = db.Column(db.Integer)

	address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
	address = db.relationship('Address', backref=db.backref('permits', lazy='dynamic'))

	def __init__(self, app_id, file_date, status_date, expiration_date):
		self.app_id = app_id
		self.file_date = file_date
		self.status_date = status_date
		self.expiration_date = expiration_date


	def __repr__(self):
		return '<Permit %r>' % self.app_id


class Address(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.String(20))
	street = db.Column(db.String(500))
	city = db.Column(db.String(200))
	state = db.Column(db.String(100))

	def __init__(self,number,street,city="San Francisco",state="California"):
		self.number = number
		self.street = street
		self.city = city
		self.state = state
	
	def full_address(self):
		return self.number+" "+self.street+" "+self.city+", "+self.state
	
	def __repr__(self):
		return '<Address %r>' % self.full_address()