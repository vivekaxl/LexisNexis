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
import sys, os
import datetime
import socket
import getpass
import time
from subprocess import STDOUT, check_call
from contextlib import contextmanager

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

This script is written to expidite the process of initial system configuration
(specifically Ubuntu). These initial things include basic setup, securing the
system(firewall), updating it etc. I have not tested this with any other distro 
but this can be modified to suit your need.Its preferrable you run this on new
system as it overwrite some files.
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

def hostname_setup():
    print "\n\n(+) Setting hostname"
    sys_hostname = raw_input("(-) Hostname: ")
    f001 = open('/etc/hostname','w')
    f001.write(sys_hostname)
    f001.close()
    os.system("hostname -F /etc/hostname")
    print "(+) Hostname set"

def timezone_setup():
    os.system("dpkg-reconfigure tzdata")
    print "\n(+) Timezone set"
    cur_time = datetime.datetime.now()
    print "(+) Current date: %s" % cur_time

def is_connected():
    REMOTE_SERVER = "www.jsinix.com"
    try:
      host = socket.gethostbyname(REMOTE_SERVER)
      s = socket.create_connection((host, 80), 2)
      return True
    except:
       pass
    return False

def update_setup():
    print "(+) Updating repository"
    os.system("apt-get update > /dev/null")
    print "(+) Update complete"
    print "(+) Installing updates"
    os.system("apt-get upgrade -y > /dev/null")
    print "(+) Complete"

def fail2ban_setup():
    print "\n(+) Installing Fail2ban"
    os.system("apt-get install fail2ban -y > /dev/null")
    print "(+) Restarting Fail2ban"
    os.system("service fail2ban restart > /dev/null")
    print "(+) Fail2ban running"

def iptables_setup():
    print "\n(+) Installing firewall"
    f002 = open('/etc/iptables.firewall.rules','w')
    f002.write(Iptable_rules)
    f002.close()
    os.system("iptables-restore < /etc/iptables.firewall.rules")
    print "(+) Firewall is running"
    print "(+) Setting up firewall on startup"

    firewall_startup = """
    #!/bin/sh
    /sbin/iptables-restore < /etc/iptables.firewall.rules
    """
    f003 = open('/etc/network/if-pre-up.d/firewall','w')
    f003.write(firewall_startup)
    f003.close()
    os.system("chmod +x /etc/network/if-pre-up.d/firewall")

internet = is_connected()
def controller():
    os.system("clear")
    print Welcome
    print Disclaimer
    option01 = raw_input("Should we start ?(y/n) ")

    if option01 == 'y':
        hostname_setup()
        time.sleep(1)
        timezone_setup()

        if internet == True:
            print "\n(+) Looks like system is connected to internet."
            update_setup()

            fail2ban_setup()

        elif internet == False:
            print "\n(+) Looks like no internet connectivity"
            print "    Dropping repo update"

    elif option01 == 'n':
        print "\n(+) Exiting"
        sys.exit()

    else:
        print "\n(+) Unknown choice"
        print "(+) Exiting"

    iptables_setup()

# This script must be run as root to avoid permission
# issues.
#So lets make sure that no other user can run it.
my_user = getpass.getuser()
if(my_user != 'root'):
    print "(+) Please run this script as ROOT"
    sys.exit()

else:
    controller()
    print "\n(+) Restart the system(recommended) !"
