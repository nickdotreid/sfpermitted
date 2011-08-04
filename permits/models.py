from permits import db

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