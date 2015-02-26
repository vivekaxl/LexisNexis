import requests
import json
#Please change the accessKey and URL of your own.

def URLShorten(URL):

	'''query_params = {'access_token': 'YOUR OWN ACCESS_TOKEN',
			   'longUrl': 'http://worrydream.com/LearnableProgramming/'} 
					'''
	query_params = {'access_token': 'YOUR OWN ACCESS_TOKEN','longUrl': URL} 
	endpoint = 'https://api-ssl.bitly.com/v3/shorten'
	response = requests.get(endpoint, params=query_params, verify=False)

	data = json.loads(response.content)
	print data
