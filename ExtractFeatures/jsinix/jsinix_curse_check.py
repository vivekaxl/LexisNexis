#!/usr/bin/python
# This script's basic function is to take a URL as input
# and download the page, then uses the wdyl.com API to 
# check if the data has any kind of curse word in it.

import socket
import urllib2
import sys, getopt
import urllib

def check_profanity(input_text):
    connection = urllib.urlopen("http://www.wdyl.com/profanity?q="+input_text)
    output = connection.read()
    print output
    connection.close()

def get_content(inp_dom):
    timeout = 10
    socket.setdefaulttimeout(timeout)

    req = urllib2.Request(inp_dom)
    response = urllib2.urlopen(req)
    content = response.read()

    return content

argno = len(sys.argv)

if(argno != 2):
    print "Usage: jsinix_curse_check.py http://domain.com"
    sys.exit()

else:
    domain = sys.argv[1]
    all_content = get_content(domain)
    check_profanity(all_content)
