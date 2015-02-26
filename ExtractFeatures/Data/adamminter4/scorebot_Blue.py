#!/usr/bin/python
# Python script for Blue Team
# Author: Naveen
import datetime
import commands


# current time
now=datetime.datetime.now()
print now.strftime("%Y-%m-%d %H:%M")

# Ask fo Ip of linux system
lipaddr=raw_input("Enter linux IP:")
print "linux ip is"+lipaddr

# Ask for Ip of windows syste,
wipaddr=raw_input("Enter Windows IP:")
print "windows ip is"+wipaddr

# httpstatus of host
arg='/usr/lib/nagios/plugins/check_http '+lipaddr+' | cut -b1-7'
httpstat=commands.getoutput(arg)

print httpstat

if httpstat=="HTTP OK":
    print "host http is looking good!"
else:
    print "host http is down!!!!"

# MYSQLstatus of host
arg='/usr/lib/nagios/plugins/check_mysql '+lipaddr+' | cut -b1-5'
mysqlstat=commands.getoutput(arg)

print mysqlstat

if mysqlstat=="Can't":
    print "host mysql is down!!!!"
else:
    print "host mysql is looking good!"

# SSHstatus of host
arg='/usr/lib/nagios/plugins/check_ssh '+lipaddr+' | cut -b1-6'
sshstat=commands.getoutput(arg)

print sshstat

if sshstat=="SSH OK":
    print "host ssh is looking good!"
else:
    print "host ssh is down!!!!"
