import mechanize
import re

#URL to get vaccination information
URL = "http://www.babycenter.in/t1012837/immunisation-scheduler"


br = mechanize.Browser()

r = br.open(URL)
from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(br.response().read())

rows = soup.findAll("div", {"class": "module"})

for row in rows:
	category = row.find("div", {"class": "modhead1"})
	category_text = category.text
	print category_text
	vaccines = row.findAll("span", {"class": "emph"})
	for vaccine in vaccines:
		print vaccine.findAll(text=True)
