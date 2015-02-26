import requests
import json

'''	given the bitly url we can find the number of clicks made in last fewminutes
	by using this program 
	input: bitlyURL, mins for which the link history has to be seen
	'''
	
	
def NoOfClicksMadeInLastFewMins(bitlyURL, timeInMins)
	query_params = {'access_token': 'API_KEY',
        		 'link': bitlyURL,'unit' : 'minute', 'units' : timeInMins} 


	#configured to make call to bitly Link API
	endpoint = 'https://api-ssl.bitly.com/v3/link/clicks'
	response = request.get(endpoint, params = query_params, verify = False)
	
	data = json.loads(response.content)
	print data
	
