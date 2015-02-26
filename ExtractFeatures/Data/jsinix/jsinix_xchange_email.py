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

# Getting updates on exchange/currency rates via 
# email and SMS on regular intervals via cronjob. 
# 1 7 * * * python /tmp/jsinix_xchange_email.py
# 1 19 * * * python /tmp/jsinix_xchange_email.py
# Twilio can be installed by 'pip install twilio'

#!/usr/bin/python
import urllib, ast
import smtplib, time
from twilio.rest import TwilioRestClient

def get_rate(input1):
    connection = urllib.urlopen("http://rate-exchange.appspot.com/currency?from=USD&to="+input1)
    data = connection.read()
    data1 = ast.literal_eval(data)
    rateval = data1["rate"]
    return rateval

pdate = time.strftime("%d/%m/%Y")
ptime = time.strftime("%H:%M:%S")
xvalue = get_rate("INR")
subb = "USD2INR : "+pdate+ " "+ptime
TEXT = "1 USD = %s INR" % xvalue

SERVER = "localhost"
FROM = "jsinix@jsinix.com"
TO = ["jsinix.1337@gmail.com"]
SUBJECT = subb
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

server = smtplib.SMTP(SERVER)
server.sendmail(FROM, TO, message)
server.quit()


def jsinix_sms(messms, rcpsms):
    account_sid = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(to=rcpsms, from_="+1xxxxxxxxxx", body=messms)

numbers = ["+14160000000", "+16470000000"]

for i in numbers:
    try:
        jsinix_sms(SUBJECT+" "+TEXT, i)
    except twilio.TwilioRestException as e:
        print e
