import csv
import time
import re

def parse_csv(file_location):
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
	return int(time.mktime(time.strptime(letters,'%d-%b-%y')))