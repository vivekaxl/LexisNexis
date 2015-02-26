#!/usr/bin/env python
# Copyright (c) 2010 Tim 'Shaggy' Bielawa <timbielawa@gmail.com>
#             2010 Andrew Butcher <abutcher@afrolegs.com>
#             2010 Ricky Hussmann <ricky.hussmann@gmail.com>
#             2010 Kel Cecil <kelcecil@praisechaos.com>
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

import urllib2;
import json;
import time;
import datetime;
import os;

from optparse import OptionParser
from xml.dom import minidom
from pprint import pprint

def main():
   # Perform the search GET
    nativeTweetData = TweetData()

    Madness = ParseArguments()

    # Until we get some more algos I'm making kels bag of words the default
    # Eventually there will be a class to register algos with called 'guess'.
    # You'll call it like guess.with('kels')
    # When you write an algo you'll register it with a name and a function reference
    # Like guess.register('kels', KelsBagOWords)
    if Madness.PrintTweets:
        PrintTweets(nativeTweetData)

    elif Madness.PrintTweetText:
        PrintTweetText(nativeTweetData)

    elif Madness.WeatherData:
        pprint(WeatherData("26506"))

    elif Madness.FuckStoppedDown:
        FuckStoppedDown(nativeTweetData)

    # Guess
    else:
        KelsBagOWords(nativeTweetData)


def ParseArguments():
    # Check sys.argv for arguments.
    parser = OptionParser()
    parser.add_option('--printtweets',
                      dest='PrintTweets',
                      action='store_true',
                      help='Print the information passed to the classifiers.  Useful if you want \
                            to know what\'s going into your classifier!')
    parser.add_option('--printtweettext',
                      dest='PrintTweetText',
                      action='store_true',
                      help='Print the plain text of the tweets returned by the Twitter query.')
    parser.add_option('--kelsbagofwords',
                      dest='KelsBagOWords',
                      action='store_true',
                      help='Kel\'s simple attempt at using a simple bag of words \
                            technique. Intended to inspire others to join in rather than giving \
                            any kind of useful data. (This is default)')
    parser.add_option('--fuckstoppeddown',
                      dest='FuckStoppedDown',
                      action='store_true',
                      help='Andrew\'s time relative stopped, fuck, down algorith.')
    parser.add_option('--weatherdata',
                       dest='WeatherData',
                       action='store_true',
                       help='Print weather information for Morgantown, WV.')

    (options, args) = parser.parse_args()
    return options

def PrintTweets(data):
    print data

def PrintTweetText(data):
    # This prints everything returned by the query.
    # If you're interested in locality, check out how I filter in KelsBagOWords(data)
    for Tweet in data[u'results']:
        print Tweet[u'from_user'], Tweet[u'text']

def WeatherData(zip_code):
    weather_url = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
    weather_ns = 'http://xml.weather.yahoo.com/ns/rss/1.0'

    url = weather_url % zip_code
    dom = minidom.parse(urllib2.urlopen(url))
    forecasts = []
    for node in dom.getElementsByTagNameNS(weather_ns, 'forecast'):
        forecasts.append({
            'date': node.getAttribute('date'),
            'low': node.getAttribute('low'),
            'high': node.getAttribute('high'),
            'condition': node.getAttribute('text')
            })
        ycondition = dom.getElementsByTagNameNS(weather_ns, 'condition')[0]
    return {
        'current_condition': ycondition.getAttribute('text'),
        'current_temp': ycondition.getAttribute('temp'),
        'forecasts': forecasts,
        'title': dom.getElementsByTagName('title')[0].firstChild.data
        }

def TweetData():
    tweet_response = urllib2.urlopen('http://search.twitter.com/search.json?q=geocode:39.633611,-79.950556,25mi%20PRT')
    tweet_data = tweet_response.read()
    nativeTweetData = json.loads(tweet_data)
    return nativeTweetData

def SetMorgantownTimezone():
    # Set the timezone to Morgantown's
    os.environ['TZ'] = 'US/Eastern'
    time.tzset()

def IsWeekday():
    SetMorgantownTimezone()
    week_index = int(time.strftime('%w'))
    return not (week_index == 0 or week_index == 6)

def IsSaturday():
    SetMorgantownTimezone()
    week_index = int(time.strftime('%w'))
    return week_index == 6

def IsNowWithinNormalOperatingHours():
    SetMorgantownTimezone()
    is_normal_hours = False
    current_time = float(time.strftime('%H.%M'))

    if IsWeekday():
        is_normal_hours = (current_time > 6.3 and current_time < 22.15)

    if IsSaturday():
        is_normal_hours = (current_time > 9.3 and current_time < 17.0)

    return is_normal_hours

def bad_words():
    words = ['down', 'stopped', 'fuck', 'stuck', 'out of service']
    return words

# This approach simply attempts a bag of words approach with no temporal constraints(which is a bad thing here since there's so few tweets)
# I can promise before even writing that method will be the suck.
# Just throwing this in to get the ball rolling :)  I have a better idea I'll throw in later if someone else gives it a go.
def KelsBagOWords(data):
    # The idea behind a bag of words technique is that we simply look to see if word x occurs in a tweet.  If more negative words than positive, the PRT is down.
    # We don't consider temporal effects ( tweets that are older than a certain age shouldn't be considered)
    # or weighing some users more heavily than others (the official WVU prt twitter account over others).
    GoodWords = ['currently running', 'normal', 'normally', 'running']
    BadWords = ['down','stop', 'hate', 'bus', 'out of service', 'closed', 'fuck', 'late', ':(']
    Balance = 0

    for tweet in data[u'results']:
        GoodSigns = 0
        BadSigns = 0
        for Good in GoodWords:
            #Weighting Good Signs since there seem to be fewer ways to express approval of the PRT.
            if Good in tweet[u'text'].lower():
                GoodSigns = GoodSigns + 3
        for Bad in BadWords:
            if Bad in tweet[u'text'].lower():
                BadSigns = BadSigns + 1
        if GoodSigns > BadSigns:
            Balance = Balance + 1
        elif BadSigns > GoodSigns:
            Balance = Balance - 1

    print "Kel's Bag O' Words method thinks..."
    result = float(abs(Balance))/float(len(data[u'results']))

    if Balance > 0:
        print "The PRT is probably running: " + str(result)
    elif Balance < 0:
        print "The PRT is probably not running: " + str(result)
    else:
        print "that you should probably just go look for yourself... No one on Twitter seems to know..."

def FuckStoppedDown(data):

    what_i_care_about = []

    # Gather what I care about...
    for tweet in data[u'results']:
        tweet_date = datetime.datetime(*time.strptime(tweet[u'created_at'],
                                                      "%a, %d %b %Y %H:%M:%S +0000")[0:6])
        tweet_text = tweet[u'text']
        what_i_care_about.append({'date': tweet_date, 'text': tweet_text})

    # Sort the tweets by date if not sorted already
    what_i_care_about = sorted(what_i_care_about, key=lambda t: t['date'])

    # Get the current and last bad tweet that meet our criteria.
    current = {}
    last = {}
    for tweet in what_i_care_about:
        for word in bad_words():
            if word in tweet['text'].lower():
                current = tweet
                break
    for tweet in what_i_care_about:
        for word in bad_words():
            if word in tweet['text'].lower() and tweet is not current:
                last = tweet
                break
            
    # Gather some datetime information. We will use delta to define
    # the window of time in which a tweet would indicate an outage.
    delta = datetime.timedelta(minutes=30)
    now = datetime.datetime(*time.localtime()[0:6])
    relative_delta = now - delta

    # Make a determination.  If we got any results at all, give a
    # determination.  If we have a last bad tweet and it occured
    # within the relative delta from now, then we assume the PRT is
    # down.
    if not current and not last:
        print "Not enough bad data to work with."
    elif current and current['date'] > relative_delta:
        print "The PRT is probably down."
    else:
        print "The PRT is probably up."

if __name__ == "__main__":
    main()
