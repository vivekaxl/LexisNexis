import requests
import json

'''	given the bitly url we can find referrers of the URL
	The 'referrer' is the site that contained the link that
	you clicked on to get to the current page. You can share 
	bitly links on any site or social network, and then look 
	at the referrers to figure out which sites are actually 
	sending traffic to the link.
	input: bitlyURL
	'''
	
	
def FindReferrers(bitlyURL)
	query_params = {'access_token': 'API_KEY',
                	'link': bitlyURL}

	endpoint = 'https://api-ssl.bitly.com/v3/link/referrers'
	response = requests.get(endpoint, params=query_params, verify=False)

	data = json.loads(response.content)
	print data
	
