# Permission to use, copy, modify and distribute this 
# software and its documentation for any purpose and 
# without fee is hereby granted, provided that the above 
# copyright notice appear in all copies that both 
# copyright notice and this permission notice appear in 
# supporting documentation. jsinix makes no representations 
# about the suitability of this software for any purpose. 
# It is provided "as is" without express or implied warranty.

# jsinix DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, 
# INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. 
# IN NO EVENT SHALL jsinix BE LIABLE FOR ANY SPECIAL, INDIRECT 
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM 
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, 
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

#!/usr/bin/python
import requests
from netaddr import *
import subprocess, getpass
import sys, os, datetime

#This script if used with a cronjob can be useful.

Welcome = """\
         _     _       _
        (_)   (_)     (_)
         _ ___ _ _ __  ___  __
        | / __| | '_ \| \ \/ /
        | \__ \ | | | | |>  <
        | |___/_|_| |_|_/_/\_\.
       _/ |
      |__/
"""

Disclaimer = """\
\nAuthor: jsinix(jsinix.1337@gmail.com)

I wrote this script to setup basic iptable rules to secure the system.
In addition to that, this script queries spamhaus's blacklisted IP/Network
addresses. These IP's are then stored in a new chain called droplist. Finally
it is referenced in the default filter table chains(i.e INPUT, OUTPUT and FORWARD).
This script or its customized version can be useful for many type of public 
facing servers including mail servers to protect from spams etc.
Please use this at yur own risk and read carefully before using. You might 
need to change some parts according to your needs. 
"""

Iptable_rules = """
*filter
-A INPUT -i lo -j ACCEPT
-A INPUT -d 127.0.0.0/8 -j REJECT
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A OUTPUT -j ACCEPT
-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7
-A INPUT -j DROP
-A FORWARD -j DROP
COMMIT
"""

ip_list = []

all_links = ["http://www.spamhaus.org/drop/drop.txt"]

def get_spamhaus_ip(link):
    f = requests.get(link)

    for each in f.text.split():
        try:    
	    temp_net = IPNetwork(each)
	    ip_list.append(temp_net)
        except:
            pass


def set_blocklist(ips):
    
    cmdstring = "iptables -A droplist -s %s -j DROP" % (ips)
    os.system(cmdstring)


def use_blocklist():
    os.system("iptables -I INPUT -j droplist")	
    os.system("iptables -I OUTPUT -j droplist")
    os.system("iptables -I FORWARD -j droplist")


def iptables_setup():

    print "\n\n\n(+) Flushing old rules in droplist\n"
    os.system("iptables -F droplist")

    print "(+) Installing firewall"
    f002 = open('/etc/iptables.firewall.rules','w')
    f002.write(Iptable_rules)
    f002.close()
    os.system("iptables-restore < /etc/iptables.firewall.rules")
    print "(+) Firewall is running"
    print "(+) Setting up firewall on startup"

    print "\n(+) Creating droplist chain"
    os.system("iptables -N droplist")

    firewall_startup = """
    #!/bin/sh
    /sbin/iptables-restore < /etc/iptables.firewall.rules
    /sbin/iptables -N droplist

    """
    f003 = open('/etc/network/if-pre-up.d/firewall','w')
    f003.write(firewall_startup)
    f003.close()
    os.system("chmod +x /etc/network/if-pre-up.d/firewall")


def controller():
    print Welcome
    print "\n" 
    print Disclaimer	

    iptables_setup()

    print "(+) Quering Spamhaus Blacklist"

    for l in all_links:
        get_spamhaus_ip(l)

    print "(+) Refreshing droplist chain"

    for net in ip_list:
        set_blocklist(net)
    
    print "(+) Applying droplist to filter chain"
    use_blocklist()

# This script must be run as root to avoid permission
# issues.
#So lets make sure that no other user can run it.
my_user = getpass.getuser()
if(my_user != 'root'):
    print "(+) Please run this script as ROOT"
    sys.exit()

else:
    os.system("clear")
    controller()
    print "\n(+) Firewall updated !"
