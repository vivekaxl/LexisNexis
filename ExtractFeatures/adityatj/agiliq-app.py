import urllib, requests, json

__author__ = 'TJ Aditya'
__version__ = '0.1'

get_data = {}

get_data['client_id'] = 'szZwr7btCFclzzMZJI07zzevkvdPj27Eumzrc5KT3hOrzPZuqp'
get_data['redirect_uri'] = 'http://localhost/callback'
get_data['client_secret'] = 'xv8QwDHEZjb9b5lKhZ0teSCauaifbXFeY3Yi9USj1OfzCGCBo6'
get_data['code'] = 'r3VXJuBydK2Fso9VberHshO6Jp7yn4ypZmrXYmNVDDOKwmv7yO'

payload = urllib.urlencode(get_data)


r = requests.get('http://join.agiliq.com/oauth/access_token/?' + payload)


access_token = r.json()['access_token']

post_data = {}

post_data['first_name'] = 'Aditya'
post_data['last_name'] = 'TJ'
post_data['projects_url'] = 'https://github.com/adityatj'
post_data['code_url'] = 'https://github.com/adityatj/agiliq-app'
files = {'resume': open('Resume.docx', 'rb')}

r = requests.post('http://join.agiliq.com/api/resume/upload/?access_token=' + access_token, files=files, data=post_data)

if r.json()['success']:
    print 'Resume uploaded!'
