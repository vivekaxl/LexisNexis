# xval.py

from random import shuffle
import reader
import zeror

def xvals(table,f,x=2,b=2,a='none'):
	rows = table.rows
	s = int(len(rows)/b)
	accuracy=[]
	while(x>0):
		x-=1
		shuffle(rows)
		b1 = 0
		while (b1 < b):
			accuracy.append(xval(b1*s+1, (b1+1)*s, rows, table, f))
			b1+=1
	print accuracyPrint(accuracy)

def xval(start,stop,rows,table,f):
	rmax=len(rows)
	r=0
	train = reader.makeTable(table.header)
	test = reader.makeTable(table.header)
	while(r<rmax):
		d=rows[r]
		r+=1
		if ((r>= start) & (r <= stop)):
			reader.addRow(d, train)
		else:
			reader.addRow(d, test)
	print test
	return f.zeror(train.klass.expected, test.klass)

def accuracyPrint(accuracy):
	output = 'accuracy\r\n'
	for a in accuracy:
		output += a + ', '
	return output