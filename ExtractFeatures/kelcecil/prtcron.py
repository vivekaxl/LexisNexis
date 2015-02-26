#!/usr/bin/env python
# Copyright (c) 2010 Tim 'Shaggy' Bielawa <timbielawa@gmail.com>
# 	      2010 Andrew Butcher <abutcher@afrolegs.com>
# 	      2010 Ricky Hussmann <ricky.hussmann@gmail.com>
# 	      2010 Kel Cecil <kelcecil@praisechaos.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import json
import pprint
from pymongo import Connection
import urllib2

def main():
    db = client()
    for tweet in tweet_data():
        if db['tweets'].find({'id': tweet['id']}).count() == 0:
            db['tweets'].insert(tweet)

def client():
    return Connection('173.255.237.153')['prtdata']

def tweet_data():
    tweet_response = urllib2.urlopen('http://search.twitter.com/search.json?q=WVUDOT&from_user_id_str=85356593')
    tweet_data = json.loads(tweet_response.read())['results']
    return tweet_data

if __name__ == "__main__":
    main()
