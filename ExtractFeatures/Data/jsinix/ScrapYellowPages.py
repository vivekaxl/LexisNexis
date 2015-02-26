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

#So basicaly what this script does is scrap 
#the address/contact details of a company or 
#something similar, goes through page by page 
#and prints it. These details usualy incluse
#name, addess, phone etc

#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import re
def jsinix_grabber(uri):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    links = soup.find_all("a")
    g_data = soup.find_all("div", {"class": "article phone1 "})
    qwerty = []
    for item in g_data:
        items = re.sub('[\n]', '', item.text)
        qwerty.append(items)
    for i in qwerty:
        print "\n" 
        print i
for counter in range(1,10):
    url = "http://www.yellowpages.ca/search/si/"+str(counter)+"/Walmart/Toronto%2C%20ON"
    jsinix_grabber(url)
