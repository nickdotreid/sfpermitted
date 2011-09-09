from permits.models import *
from permits.parsing import *
import os
import glob

def parse_dir(directory):
	for xlsfile in glob.glob(os.path.join(directory,'*.xls')):
		data = parse_xls(xlsfile)
		for row in data:
			add_permit(row)
