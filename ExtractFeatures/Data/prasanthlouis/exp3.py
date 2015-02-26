from selenium import webdriver
from PIL import Image
import subprocess

def find():
	for x in elems:
		for y in ids:
			for z in values:
				if x.get_attribute(y).lower().find(z)!=-1:
					#print "hurrary"
					count=0
					driver.save_screenshot('screenshot.png')
					im = Image.open("screenshot.png")
					width=int(x.get_attribute("width"))
					height=int(x.get_attribute("height"))
					yaxis=x.location['y']
					xaxis=x.location['x']
					bbox = (xaxis,yaxis,xaxis+width,yaxis+height)
					img=im.crop(bbox)
					count=count+1
					img.save("crop"+str(count)+".gif")
					return


driver = webdriver.Firefox()
driver.get("https://www.na.citiprepaid.com/gov/")
elems=driver.find_elements_by_tag_name("img");
values=['captchaimage','captcha','cap']
ids=['id','alt','src','class']

find()


		

driver.close()


cmd = 'python exp2.py'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, err = p.communicate() 
result = out.split('\n')
for lin in result:
    if not lin.startswith('#'):
        print(lin)
