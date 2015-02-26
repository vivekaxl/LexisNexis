#!/usr/bin/env python
import os,sys
import subprocess
import get_download
x=get_download.AudioHandler()
link,size=x.getAudioStream(sys.argv[1].split("/")[-1])
subprocess.call(["vlc",str(link)])
