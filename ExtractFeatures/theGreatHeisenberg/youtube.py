from urllib2 import urlopen
import sys
import logging
from bs4 import BeautifulSoup as Soup
import pafy
from requests import session
from pickle import dump,load
class AudioHandler:
    links_dict = {}
    def __init__(self,music_list):
        self.url = "http://www.youtube.com"
        self.music_list = music_list
        self.s = session()
        self.s.get(self.url)
        self.pickle()

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

    def getLinksSize(self):
        for name in self.music_list:
            link = self.search_youtube_link(name)
            stream_url,size = self.getAudioStream(self,link)
            self.links_dict[name] = (stream_url,size)

    def pickle(self):
        self.getLinksSize()
        temp = {}
        try:
            fobj = open("dump_file","r")
            d = load(fobj)
            temp = dict(load(fobj).items + self.links_dict.items())
            fobj.close()
            fobj = open("dump_file","w")
            dump(temp,fobj)
            fobj.close()
        except:
            fobj = open("dump_file","w")
            dump(self.links_dict,fobj)
            fobj.close()

    def search_youtube_link(self,name):
        req = self.s.get("http://www.youtube.com/results?", params={"search_query": "%s" % (name)})
        soup = Soup(req.text)
        links = []
        body=soup.find('ol',{'id':"search-results"})
        k=body.a
        links.append(k.get('href'))
        return "https://www.youtube.com" + links[0]

    @staticmethod
    def getAudioStream(self,youtubeLink):
        videoLink=youtubeLink
        video = pafy.new(videoLink)
        audiostreams = video.audiostreams
#        for k in audiostreams:
#            print(k.bitrate)
        return audiostreams[0].url,audiostreams[0].get_filesize()

dict1 = {}
logging.basicConfig(filename="logs.txt",level=logging.DEBUG,filemode="w") #created a logger in debug mode.
dm= ['rushikesh','rajesh']
AudioHandler(dm)
f = open("dump_file","r")
p1 = load(f)
print(p1)


