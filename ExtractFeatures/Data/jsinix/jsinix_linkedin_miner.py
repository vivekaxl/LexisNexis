# Permission to use, copy, modify and distribute this 
# software and its documentation for any purpose and 
# without fee is hereby granted, provided that the above 
# copyright notice appear in all copies that both 
# copyright notice and this permission notice appear in 
# supporting documentation. jsinix makes no representations 
# about the suitability of this software for any purpose. 
# It is provided "as is" without express or implied warranty.

# jsinix DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. 
# IN NO EVENT SHALL jsinix BE LIABLE FOR ANY SPECIAL, INDIRECT 
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#!/usr/bin/python
from linkedin import linkedin
import json, os.path, argparse
from prettytable import PrettyTable
import urllib, urlparse, sys

Welcome = """
         _     _       _
        (_)   (_)     (_)
         _ ___ _ _ __  ___  __
        | / __| | '_ \| \ \/ /
        | \__ \ | | | | |>  <
        | |___/_|_| |_|_/_/\_\.
       _/ |
      |__/
"""

Disclaimer = """
Author: jsinix(jsinix.1337@gmail.com)

This script is used to mine data from linkedin. It gets
the information about your connections. The functionality
of the script can be improved as per your liking. This is
just a POC and the LinkedIN API can be used to do more
stuff. 

This script is only for educational purposes only. 
"""

# You must goto https://www.linkedin.com/secure/developer
# and generate your own keys and replaces the X's here.
CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
USER_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
USER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXX'
fname = "linkedin_connections.json"
yonbit = os.path.isfile(fname) 


def get_user_auth():
    
    RETURN_URL = ''
    auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,
                                    USER_TOKEN, USER_SECRET,
                                    RETURN_URL,
                                    permissions=linkedin.PERMISSIONS.enums.values())
    print "(+) Authenticating to LinkedIN "
    app = linkedin.LinkedInApplication(auth)
    return app


def get_data_from_linkedin():
    
    app = get_user_auth()
    print "(+) Grabbing all contacts"
    connections = app.get_connections()
    print "(+) Saving data to: ",fname
    try:  
        f = open(fname, 'w')
        f.write(json.dumps(connections, indent=1))
        f.close()
    except Exception as ee:
	print "(+) Error: ", ee


def data_already_present(): 
    
    print "(+) Reading data"
    connections = json.loads(open(fname).read())
    print "(+) Parsing data \n\n"
    pt = PrettyTable(field_names=['Name', 'Location'])
    pt.align = 'l'
    [ pt.add_row((c['firstName'] + ' ' + c['lastName'], c['location']['name'])) 
      for c in connections['values']
          if c.has_key('location')]
    print pt


def download_url(uri02, fname1, lname1):
   
    print "(+) Downloading Picture: %s %s" % (fname1, lname1)
    file1 = urllib.URLopener()
    path = urlparse.urlparse(uri02).path
    fn = fname1+lname1
    file1.retrieve(uri02, fn)


def download_linledin_pictures(looper1):
    
    connections = json.loads(open(fname).read())
    if connections['values'][looper1]['pictureUrl'] :
       try:
           download_url(connections['values'][looper1]['pictureUrl'], connections['values'][looper1]['firstName'], connections['values'][looper1]['lastName'])
       except Exception as e:
           print "(+) Error: %s %s :: %s" %(connections['values'][looper1]['firstName'], connections['values'][looper1]['lastName'], e)

def get_pictures():

    connections = json.loads(open(fname).read())
    for zz in range(len(connections['values'])):
        try:
            download_linledin_pictures(zz)
        except Exception as e:
            #pass
	    print "(+) Error: %s :: pictureUrl" % e

def list_all():
    
    try: 
        if yonbit == False:
	    get_data_from_linkedin(get_user_auth())	
        elif yonbit == True:
	    data_already_present()		
    except Exception as e:
	print "Error: ", e			


def print_Connection_details(looper1):
    connections = json.loads(open(fname).read())
    print "Name: ", connections['values'][looper1]['firstName'], connections['values'][looper1]['lastName']
    print "Position: ", connections['values'][looper1]['headline']
    print "Industry: ", connections['values'][looper1]['industry']
    print "Location: ", connections['values'][looper1]['location']['name']


def get_details():

    if yonbit == False:
	print "(+) The parsed file is not present locally. \n(+) Use -g or --get to get the file first."
        get_data_from_linkedin()
  
    connections = json.loads(open(fname).read())
    for zz in range(len(connections['values'])):
        try:
	    print "\n"	
            print_Connection_details(zz)
        except Exception as e:
            pass


def process_arguments(args):
    parser = argparse.ArgumentParser(description="This is LinkedIN mining tool. Use it wisely")
    
    parser.add_argument('-l',
			'--list-all',
			action='store_true',
			help="Lists all the connections along with location in a table"
                        )

    parser.add_argument('-d',
		        '--details',
		        action='store_true',
			help='Lists all the connections with the details of each'
		        )

    parser.add_argument('-p',
                        '--picture',
                        action='store_true',
                        help='Download the pictures of all the possible connections'
                        )

    parser.add_argument('-g',
                        '--get',
                        action='store_true',
                        help='Dumps the entire data locally in filename linkedin_connections.json'
                        )
	

    parser.add_argument('-v',
			'--verbose',
			dest='verbose',
			action='store_true',
			default=False,
			help='Displays all the information'
			)

    options = parser.parse_args(args)
    return vars(options)

if len(sys.argv) < 2:
    process_arguments(['-h'])
userOptions = process_arguments(sys.argv[1:])

if userOptions["get"] == True:
    get_data_from_linkedin()

if userOptions["list_all"] == True:
    list_all()

if userOptions["details"] == True:
    get_details()

if userOptions["picture"] == True:
    get_pictures()
