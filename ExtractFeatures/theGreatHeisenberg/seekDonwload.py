
import urllib2

class HttpFile(object):
    def __init__(self, url):
        self.url = url
        self.offset = 0
        self._size = -1

    def size(self):
        if self._size < 0:
            f = urllib2.urlopen(self.url)
            self._size = int(f.headers["Content-length"])
        return self._size

    def read(self, count=-1):
        req = urllib2.Request(self.url)
        if count < 0:
            end = self.size() - 1
        else:
            end = self.offset + count - 1
        req.headers['Range'] = "bytes=%s-%s" % (self.offset, end)
        f = urllib2.urlopen(req)
        data = f.read()
        # FIXME: should check that we got the range expected, etc.
        chunk = len(data)
        print chunk, count
        if count >= 0:
            assert chunk <= count
        self.offset += chunk
        return data

    def seek(self, offset, whence=0):
        if whence == 0:
            self.offset = offset
        elif whence == 1:
            self.offset += offset
        elif whence == 2:
            self.offset = self.size() + offset
        else:
            raise Exception("Invalid whence")

    def tell(self):
        return self.offset
#h = HttpFile("http://srv71.listentoyoutube.com/download/4pSZb3BlnGRkr6yq3JqUtGpjoWhnZG5tn5rfhKKj3Jeih6iR1djXrZuV/")
#print(h.size())
#print(h.seek(0,0))
#print(h.tell())
