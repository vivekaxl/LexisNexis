# zeror.py

def zeror(expected, test):
	return "{0:.2f}".format(test.data.count(expected)/float(len(test.data)))