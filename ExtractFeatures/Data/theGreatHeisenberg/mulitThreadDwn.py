import urllib2
import threading

print "rushikesh patil"
def download(start):
    req = urllib2.Request("http://srv71.listentoyoutube.com/download/4pSZb3BlnGRkr6yq3JqUtGpjoWhnZG5tn5rfhKKj3Jeih6iR1djXrZuV/")
    req.headers['Range'] = 'bytes=%s-%s' % (start, start+chunk_size)
    f = urllib2.urlopen(req)
    parts[start] = f.read()

threads = []
parts = {}
chunk_size = 8192*6
# Initialize threads
for i in range(0,20):
    t = threading.Thread(download(i*chunk_size))
    t.start()
    threads.append( t)

# Join threads back (order doesn't matter, you just want them all)
for i in threads:
    i.join()

# Sort parts and you're done
result = ''

for i in range(0,10):
    result += parts[i*chunk_size]
f = open("son1.mp3","wb")
f.write(result)
