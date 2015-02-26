import urllib2
import re
import time
import xml.etree.ElementTree as ET

tree = ET.parse('country_data.xml')
root = tree.getroot()


# zetcode.com/db/mysqlpython/
#import xml.etree.ElementTree as etree
# or for a faster C implementation


#tree = etree.parse('input.xml')
#elem = tree.find('//tag-Name') # finds the first occurrence of element tag-Name
#elem.text = 'newName'
#tree.write('output.xml')

model=list()
price=list()
carlink=list()
abstractInformation=list()
timePost=list()
today=True
num=0
#print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
mystrTime=time.strftime('%Y-%m-%d %X',time.localtime(time.time()))

for user in root.findall('user'):
    temp=user.find('lastvisitTime')
    lastvisitTime=temp.text
    print temp.text
    temp.text=mystrTime
    print user.find('lastvisitTime').text

while today:
    if num==0:
        tempstr='http://raleigh.craigslist.org/search/cto//'
    else:
        tempstr='http://raleigh.craigslist.org/search/cto?s='+str(num)+'//'
    
    response = urllib2.urlopen(tempstr)
    html = response.read()
#print html
#<span class="price">crifan</span>
#0 
#print html

#m = re.match(r'hello', 'hello world!')
#print m.group()

#foundH1user = re.findall('<span\s+?class="price">(?P<price>.+?)</span>',html)
#   <p class="row" data-pid=" ... </p>
#print foundH1user

#1 line
#Terms=re.findall(r'<p\s*class="row"\s*data-pid="\w+">',html)
#print type(Terms)
#for i in range(len(Terms)):
#    print Terms[i]

#2 line
#Terms2=re.findall(r'<a href="/\w+/\w+\.html"\s*class="i"\s*data-id="\w+\:\w+">',html)
#for i in range(len(Terms2)):
#    print Terms2[i]

#3 line
#Terms3=re.findall('<span\s+?class="price">(?P<price>.+?)</span>',html)
#for i in range(len(Terms3)):
#    print Terms3[i]

#misunderstanding 
#Terms4=re.findall('<span\s+?class="price">(?P<price>.+?)</span></a>',html)
#for i in range(len(Terms3)):
#    print Terms3[i]

#Terms4=re.findall('<span class="txt"> <span class="star"></span> <span class="pl">',html)
#print len(Terms4)

#Terms5=re.findall(r'<time\s*datetime="\w+-\w+-\w+\s*\w+\:\w+" title="\w+ \w+ \w+ \w+\:\w+\:\w+ \w+ \(\w+ \w+ \w+\)">\w+ \w+</time>',html)

#for i in range(len(Terms5)):
#    print Terms5[i]
#print len(Terms5)    

#Terms6=re.findall(r'<a href="/\w+/\w+.html"\s*data-id="\w+"\s*class="\w+">.+?</a>\s*</span>\s*<span\s*class="l2">',html)
#for i in range(len(Terms6)):
#    print Terms6[i]
#print len(Terms6)
# some special characters?
#Terms7=re.findall(r'<span class="pnr"> <small> (.+?)</small>',html)
#print len(Terms7)
#for i in range(len(Terms7)):
#    print Terms7[i]

    Terms8=re.findall(r'<span class="txt"> <span class="star"></span> <span class="pl"> <time\s*datetime=".+?" title=".+?">.+?</time> <a href=".+?"\s*data-id="\w+"\s*class="\w+">.+?</a>\s*</span>\s*<span\s*class="l2"> .+?</p>',html)
    for i in range(len(Terms8)):
        timeCur=re.search(r'<time\s*datetime="(.+?)" title="(.+?)">(.+?)</time> <a href="(.+?)"\s*data-id="(\w+)"\s*class="(\w+)">(.+?)</a>\s*</span>\s*<span\s*class="l2">\s*<span\s*?class="price">&#x0024;(\w+?)</span>',Terms8[i])
        if timeCur:
            print lastvisitTime
            print timeCur.group(1)
            if timeCur.group(1)<=lastvisitTime:
                today=False
                break
            if (('altima' in timeCur.group(7).lower()) or ('volkswagen' in timeCur.group(7).lower()) or ('camry' in timeCur.group(7).lower()) or ('accord' in timeCur.group(7).lower())) and (int(timeCur.group(8))>6000):
                timePost.append(timeCur.group(3))
                price.append(timeCur.group(8))
                carlink.append(timeCur.group(4))
                abstractInformation.append(timeCur.group(7))
                print timeCur.group(1)
                print timeCur.group(2)
                print timeCur.group(3)
                print timeCur.group(4)
                print timeCur.group(5)
                print timeCur.group(6)
                print timeCur.group(7)
                print timeCur.group(8)    
        print '------------------------------'
    print num    
    num=num+100

#coding: utf-8 
import smtplib 
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.audio import MIMEAudio 
from email.mime.base import MIMEBase 
from email.mime.multipart import MIMEMultipart 

import os, mimetypes 

username = 'dragonfly90mad@gmail.com' # ÓûﾧÃû 
password = '********' # ÃÜÂë 

sender = 'dragonfly90mad@gmail.com' # ﾷﾢﾼþÈËÓÊÏä 
receiver = 'ldong6@ncsu.edu' # ÊռþÈËÓÊÏä 
subject = 'python email test'
mail_content='<html>'
for i in range(len(timePost)):
    mail_content =mail_content+'<p>'+timePost[i]+' , '+price[i]+' dollars,  '+abstractInformation[i]+',  <a href="http://raleigh.craigslist.org'+carlink[i]+'">http://raleigh.craigslist.org'+carlink[i]+'</a></p>' # emailÄÚÈÝ 
mail_content=mail_content+'</html>'
msgText = MIMEText(mail_content,'html','utf-8') 

msg = MIMEMultipart() 
msg['Subject'] = subject 
msg.attach(msgText) 

filepath = unicode('Liang.jpg','utf8') 
ctype, encoding = mimetypes.guess_type(filepath) 
if ctype is None or encoding is not None: 
    ctype = "application/octet-stream" 
maintype, subtype = ctype.split("/", 1) 

if maintype == 'text': 
    fp = open(filepath) 
    attachment = MIMEText(fp.read(), _subtype=subtype) 
    fp.close() 
elif maintype == 'image': 
    fp = open(filepath, 'rb') 
    attachment = MIMEImage(fp.read(), _subtype=subtype) 
    fp.close() 
elif maintype == 'audio': 
    fp = open(filepath, 'rb') 
    attachment = MIMEAudio(fp.read(), _subtype=subtype) 
    fp.close() 
else: 
    fp = open(filepath, 'rb') 
    attachment = MIMEBase(maintype, subtype) 
    attachment.set_payload(fp.read()) 
    fp.close() 
    encoders.encode_base64(attachment) 
attachment.add_header('Content-Disposition', 'attachment', filepath=filepath) 
#msg.attach(attachment) 
#don't use attachment
mail_server = 'smtp.gmail.com' 
mail_server_port = 587 
server = smtplib.SMTP(mail_server, mail_server_port) 
# server.set_debuglevel(1) # ﾵ÷ÊÔģʽ 
server.ehlo() 
server.starttls() 
server.login(username, password) 
server.sendmail(sender, receiver, msg.as_string()) 
server.quit()
               
