import csv
import time
import datetime
import re
import xlrd

def parse_xls(file_location):
	wb = xlrd.open_workbook(file_location)
	sh = wb.sheet_by_index(0)
	keys = sh.row_values(0)
	for rownum in range(sh.nrows):
		if rownum is not 0:
			row = sh.row_values(rownum)
			#matach keys
			dictionary = {}
			for cellnum in range(len(row)):
				dictionary[keys[cellnum]] = row[cellnum]
			yield permit_xls_clean_row(dictionary,wb)
			
def permit_xls_clean_row(row,workbook):
	clean = {}
	for key in row.keys():
		if row[key]:
			if re.search('(APP)',key):
				clean['app_id'] = row[key].lstrip('# ')
			if re.search('FILE',key):
				clean['file_date'] = make_unix_from_xls_float(row[key],workbook.datemode)
			if re.search('EXPIRATION',key):
				clean['expiration_date'] = make_unix_from_xls_float(row[key],workbook.datemode)
			if re.search('STATUS_DATE',key):
				clean['status_date'] = make_unix_from_xls_float(row[key],workbook.datemode)
			if re.search('STREET_NUMBER',key):
				clean['street_number'] = row[key]
			if re.search('AVS_STREET_NAME',key):
				clean['street_name'] = row[key]
			if re.search('AVS_STREET_SFX',key):
				clean['street_suffix'] = row[key]
	return clean
	
def parse_csv(file_location):
	data = csv.DictReader(open(file_location))
	count = 0
	for row in data:
		yield permit_row_clean(row)
		
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
	
def make_unix_from_xls_float(decimal,datemode):
	return int(datetime.datetime(*xlrd.xldate_as_tuple(decimal,datemode)).strftime('%s'))
	