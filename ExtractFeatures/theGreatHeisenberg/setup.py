import os
import re
import subprocess
from os.path import expanduser
import apt
#remove garbage
subprocess.Popen("sudo rm -r /usr/share/pyMusicFs",shell=True).wait()
subprocess.Popen("sudo rm /usr/share/applications/stream_vlc.desktop",shell=True).wait()

#prerequisites

cache = apt.Cache()

if not cache['python-fuse'].is_installed:
    fuse_commands = ["sudo apt-get install python-fuse"]
    for command in fuse_commands:
        p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        p.wait()
else:
    print "python-fuse requirement is already satisfied"

if not cache['python-pip'].is_installed:
    pip_commands = ["sudo apt-get install python-pip"]
    for command in pip_commands:    
        p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        p.wait()
else:
    print "python-pip requirement is already satisfied"

if not cache['vlc'].is_installed:
    pip_commands = ["sudo apt-get install vlc"]
    for command in pip_commands:    
        p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        p.wait()
else:
    print "VLC requirement is already satisfied"


import pip
installed_packages = pip.get_installed_distributions()
installed_packages_list = sorted(["%s" % (i.key)
     for i in installed_packages])

req_packages = ["bs4","pafy","requests"]
for package in req_packages:
    if package not in installed_packages_list: 
        p=subprocess.Popen("sudo pip install %s"%package,shell=True,stdout=subprocess.PIPE)
        p.wait()
    else:
        print "%s requirement is already satisfied"%package


if not cache['python2.7-dev'].is_installed:
    pythonDev_commands = ["echo \"deb http://us.archive.ubuntu.com/ubuntu/ precise-updates main restricted\" | sudo tee -a /etc/apt/sources.list.d/precise-updates.list ","sudo apt-get update","sudo apt-get install python2.7-dev"]
    for command in pythonDev_commands:
        p=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        p.wait()
else:
    print "python2.7-dev requirement is already satisfied"

commands=[("sudo mkdir /usr/share/pyMusicFs","creating directory structure"),("sudo cp -r src /usr/share/pyMusicFs/","Copying source directory"),("sudo mkdir /usr/share/pyMusicFs/icons/",".."),("sudo cp src/stream_vlc.desktop /usr/share/applications/stream_vlc.desktop","copying desktop file"),("sudo cp icons/stream_vlc.ico /usr/share/pyMusicFs/icons/stream_vlc.ico","..")]
for command,text in commands:
    p=subprocess.Popen(command,shell=True)
    p.wait()
    print text

print "creating entry in mimeapp list "
obj=open(expanduser("~")+"/.local/share/applications/mimeapps.list")
buff=obj.read()
obj.close()
flag=0
buff2=""
for line in buff.split("\n"):
    if line=="[Default Applications]":
        flag=1
    if flag==1:
        line=line.replace("vlc.desktop","stream_vlc.desktop")
    buff2=buff2+line+"\n"
print buff2

obj=open(expanduser("~")+"/.local/share/applications/mimeapps.list","w")
obj.write(buff2)
obj.close()
p=subprocess.Popen("sudo chmod +x /usr/share/pyMusicFs/src/script.py",shell=True)
p.wait()
