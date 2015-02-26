#!/usr/bin/env python

import os, stat, errno, find_music
import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG,filemode='w')
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse

from get_download import AudioHandler

if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)
import seekDonwload

config = ["suits/all","trudetectvie/all","lost/Season 3","sherlockbbc/all","breakingbad/all","friends/all"]
table={}
for everyItem in config:
    series,season=everyItem.split("/")
    x=find_music.find_music(name=series,type='tv')
    series=x.get_OriginalName()
    if series not in table:
        table[series]=[season]
    else:
        table[series].append(season)
class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0
class HelloFS(Fuse):
    def __init__(self,*args,**kw):
        self.metaInfo={}
        Fuse.__init__(self,version="%prog " + fuse.__version__,
                     usage=args[0],
                     dash_s_do='setsingle')
    def getattr(self, path):
        logging.info("getattr called "+str(path))
        print "path=",path
        st = MyStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif path.count("/")<=3:
           st.st_mode=stat.S_IFDIR | 0755
           st.st_nlink = 2
        elif path.count("/")==4:
            st.st_mode=stat.S_IFREG | 0755
            st.st_nlink = 2
            '''try:
                logging.info("before")
                global metaInfo
                link,st.st_size=self.metaInfo[path.split("/")[-1]]
                logging,info("after")
            except:
                logging.info("in except 1")
                link,st.st_size=AudioHandler().getAudioStream(path.split("/")[-1])
                logging.info("in except 2")
                global metaInfo
                self.metaInfo[path.split("/")[-1]]=(link,st.st_size)
                logging.info("in except 3")
            '''
        else:
            return -errno.ENOENT
        return st

    def readdir(self, path, offset):
        logging.info("called 0")
        if path=="/":
            logging.info(" called"+str(path))
            self.dictionary=[i for i in table.keys()]
        elif path.count("/")==1:
            logging.info(" called"+str(path))
            nameOfSeries=path.split("/")[-1]
            self.seriesObject=find_music.find_music(nameOfSeries,"tv")
            if table[nameOfSeries]==["all"]:
                self.dictionary=self.seriesObject.get_seasons()
            else:
                self.dictionary=[]
                validList=self.seriesObject.get_seasons()
                for currentSeason in table[nameOfSeries]:
                    if currentSeason in validList:
                        self.dictionary.append(currentSeason)
        elif path.count("/")==2:
            logging.info(" called"+str(path))
            empty,nameOfSeries,currentSeason=path.split("/")
            #seriesObject=find_music.find_music(nameOfSeries,"tv")
            self.dictionary=self.seriesObject.get_episodes(currentSeason)
        elif path.count("/")==3:
            logging.info(" called"+str(path))
            empty,nameOfSeries,currentSeason,currentEpisode=path.split("/")
            logging.info("called 1")
            #seriesObject=find_music.find_music(nameOfSeries,"tv")
            logging.info("called 2")
            self.dictionary=self.seriesObject.getMusicdict(currentSeason,currentEpisode)
            logging.info("called 3")
        for r in ['.','..']+self.dictionary:
                yield fuse.Direntry(r)

    def open(self, path, flags):
        logging.info("open called")
        #link,size=get_download().donwload_by_name(path.split("/")[-1])
        #self.h = seekDonwload.HttpFile(link)
        logging.info("open completed")

    def read(self, path, size, offset):
        logging.info("read called size,offset "+str(size)+" "+str(offset))
        self.h.seek(offset,whence=0)
        return self.h.read(size)
        #logging.info("read completed")

    def truncate(self,path,size):
        return 0

    def release(self,path,flags):
        x=""
        self.h=""
        return 0
def main():
    usage="""
Userspace hello example
""" + Fuse.fusage
    server = HelloFS(usage)
    #print table
    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
