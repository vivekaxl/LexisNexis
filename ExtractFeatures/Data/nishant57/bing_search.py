import json
import urllib, urllib2

def run_query(search_terms):
	root_url='https://api.datamarket.azure.com/Bing/Search/'
	source = 'Web'
	
	results_per_page = 10
	offset = 0

	query = "'{0}'".format(search_terms)
	query = urllib.quote(query)

	search_url = "{0}{1}?$format=json&$skip={3}&Query={4}".format(
		root_url,
		source,
		results_per_page,
		offset,
		query)

	username = ''
	bing_api_key = '16XQEIkq9c2VcwlVuKEhLbCTjHbOB4NFVD08q3fRQt8'
	
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, search_url, username, bing_api_key)

	results = []

	try:
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)

		response = urllib2.urlopen(search_url).read()

		json_response = json.loads(response)

		for result in json_response['d']['results']:
			results.append({
				'title': result['Title'],
				'link': result['Url'],
				'summary': result['Description']
				})

	except urllib2.URLError, e:
		print "Error while querying the Bing API: ", e

	return results
