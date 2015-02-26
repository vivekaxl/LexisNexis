#!/usr/bin/python
import urllib

This tiny piece of code resolves the MAC address to its vendor. 

def Get_Vendor(macaddr):
    connection = urllib.urlopen("http://api.macvendors.com/"+macaddr)
    output = connection.read()
    connection.close()
    return output

my_mac = "xx:xx:xx:xx:xx:xx"

print Get_Vendor(my_mac)
