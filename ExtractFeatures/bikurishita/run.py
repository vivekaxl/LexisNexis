# run.py

import sys
sys.path.append("/home/jeff/")
import reader
import xval
import zeror

if __name__ == "__main__":
	try:
		filename = sys.argv[-1]
		table = reader.reader(filename)
		xval.xvals(table, zeror)
	except IndexError:
		print "Must specify csv file"
		sys.exit(1)