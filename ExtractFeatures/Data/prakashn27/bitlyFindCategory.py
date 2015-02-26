import requests
import json

'''	given the bitly url we can find category of the web page
	input: bitlyURL
	'''
	
	
def FindCategory(bitlyURL)
	query_params = {'access_token': 'API_KEY',
        		 'link': bitlyURL}

	endpoint = 'https://api-ssl.bitly.com/v3/link/category'
	response = requests.get(endpoint, params=query_params, verify=False)

	data = json.loads(response.content)
	print data
	
