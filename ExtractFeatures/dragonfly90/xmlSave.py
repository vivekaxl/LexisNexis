import xml.etree.ElementTree as ET
import time
mystrTime=time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
tree = ET.parse('country_data.xml')
root = tree.getroot()
for user in root.findall('user'):
    temp=user.find('lastvisitTime')
    print temp.text
    temp.text=mystrTime
    print user.find('lastvisitTime').text
tree.write('country_data.xml');
