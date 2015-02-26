import requests
import json

'''	given the bitly url we can find the number of clicks 
	by using this program '''
	
def NoOfClicks(bitlyURL)
	query_params = {'access_token': 'YOUR OWN ACCESS_TOKEN',
        		 'link': bitlyURL} 

	#configured to make call to bitly Link API
	endpoint = 'https://api-ssl.bitly.com/v3/link/clicks'
	response = request.get(endpoint, params = query_params, verify = False)
	
	data = json.loads(response.content)
	print data
	
