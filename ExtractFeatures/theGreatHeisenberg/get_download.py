from urllib2 import urlopen
import sys
from requests import get
from bs4 import BeautifulSoup as Soup
import pafy
class AudioHandler:
    def __init__(self):
        pass
    def download(self,raw_url,name):
        file_name = name
        url = raw_url.replace(' ','%20')
        u = urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)


            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            sys.stdout.write('\r'+status)
        f.close()

    def download_list(self,dwn_list):
        for url in dwn_list:
            self.download(url)

    def search_youtube_link(self,name):
        req = get("http://www.youtube.com/results?", params={"search_query": "%s" % (name)})
        soup = Soup(req.text)
        links = []
                
        body=soup.find('ol',{'class':"section-list"})
        #print body
        k=body.a
        #print k
        links.append(k.get('href'))
        #print links[0]
        return "https://www.youtube.com" + links[0]

    
    def getAudioStream(self,name):
        videoLink=self.search_youtube_link(name)
        video = pafy.new(videoLink)
        
        audiostreams = video.audiostreams
      #  for k in audiostreams:
      #      print(k.bitrate)
        return audiostreams[0].url,audiostreams[0].get_filesize()


#d = AudioHandler()
#print AudioHandler().getAudioStream('rushikesh')
