from permits import db
from geopy import geocoders

def add_permit(data):
	if 'app_id' in data and 'status_date' in data and 'file_date' in data and 'expiration_date' in data:
		if Permit.query.filter_by(app_id = data['app_id']).first() is None:
			permit = Permit(data['app_id'],data['file_date'],data['status_date'],data['expiration_date'])
			permit.address = add_address(data)
			db.session.add(permit)
			db.session.commit()
			return True
	return False
	
def add_address(data):
	if 'street_number' in data and 'street_name' in data and 'street_suffix' in data:
		address = Address.query.filter_by(number = data['street_number'], street = data['street_name']+" "+data['street_suffix']).first()
		if address is None:
			address = Address(data['street_number'],data['street_name']+" "+data['street_suffix'])
			db.session.add(address)
			db.session.commit()
		return address
	return None
	
def locate_addresses():
	addresses = Address.query.filter_by(geolocation=None).limit(100).all()
	for address in addresses:
		geocode_address(address)
	
	
def geocode_address(address):
	g = geocoders.Google()
	results = g.geocode(address.full_address(), exactly_one = False)
	for result in results:
		place, (lat, lng) = result
		geo = GeoLocation(lat,lng)
		geo.address = address
		db.session.add(geo)
		db.session.commit()

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
	
	geolocation_id = db.Column(db.Integer, db.ForeignKey('address.id'))
	geolocation = db.relationship('GeoLocation', uselist=False, back_populates='address')

	def __init__(self,number,street,city="San Francisco",state="California"):
		self.number = number
		self.street = street
		self.city = city
		self.state = state
	
	def full_address(self):
		return self.number+" "+self.street+" "+self.city+", "+self.state
	
	def __repr__(self):
		return '<Address %r>' % self.full_address()
		
class GeoLocation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	
	address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
	address = db.relationship('Address', uselist=False,back_populates='geolocation')
	
	def __init__(self,latitude,longitude):
		self.latitude = latitude
		self.longitude = longitude
		
	def __repr__(self):
		return '<GeoLocation %r>' % self.id
	