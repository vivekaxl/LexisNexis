import urllib2

def getpage(url):
    for i in range(100):
        try:
            req = urllib2.Request(url)
            obj = urllib2.urlopen(req)
            page = obj.read()
        except IOError:
            print 'connection failure'

getpage('http://uthcode.sarovar.org')
getpage('http://uthcode.sarovar.org')
