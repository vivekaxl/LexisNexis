dob = '24-JAN-96'
 
dob = dob.split('-')
date = dob[0]
month = dob[1]
year = int(dob[2])
year_to_concat = dob[2]
if (year>50):
	year = '19'+ year_to_concat
	print year
elif(year<50 and year>00):
	year = '20'+ year_to_concat
	print year
 
 
months = {
	 	'JAN': '01',
	 	'FEB': '02',
	 	'MAR': '03',
	 	'APR': '04',
	 	'MAY': '05',
	 	'JUN': '06',
	 	'JUL': '07',
	 	'AUG': '08',
	 	'SEP': '09',
	 	'OCT': '10',
	 	'NOV': '11',
	 	'DEC': '12'
	 	}
 
if month in months:
	month = months[month]

dob = year + '-' + month + '-' + date
print dob