'''	use bitly's search engine to find links 
	about anything, ranked by their current popularity.
	

	Whatever you search for is called a "query". 
	Replace the query parameter with whatever you would like to find.
    The limit parameter is the number of results to return. 
	It's set to 1 by default, but feel free to change it to be as many as 10.

	'''
import requests
import json

def Search(keyword)
	query_params = {'access_token': 'API_KEY',
        		'query': keyword,
        		'limit': 1}

	endpoint = 'https://api-ssl.bitly.com/v3/search'
	response = requests.get(endpoint, params=query_params, verify=False)

	data = json.loads(response.content)
	print data
	
