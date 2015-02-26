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
import os, random, struct
from Crypto.Cipher import AES
import email.parser
import os, sys, getpass
import base64
import dropbox
#Using: pip install dropbox

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

This script is a neat and cheap way to backup all the  
attachments of all emails and optionally encrypt them.
After that these files are send over to your dropbox 
account. You will have to generate your own token by 
going to https://www.dropbox.com/developers/apps and 
replace it in the script. 
"""

all_emails = []
pwd = os.getcwd()
to_store = "/root/scripts/jsinix/"
vhostdir = "/var/mail/vhosts/jsinix.com/"
enc_key = '9876543210qwerty'

#This function is used to upload the files 
#to your dropbox account. Note that you can 
#chage the arguments to change the detination 
#directory as per your needs. 
def jsinix_dropbox_uploader(input_file):

    client = dropbox.client.DropboxClient('xxxxxxxxxx-HereGoesYourToken-xxxxxxxxxx')
    account_dict = client.account_info()

    for key, value in account_dict.iteritems() :
        if key=='display_name':
            print "\n(+) Linked Account: %s" % value	
	    

    ToBeUploaded = input_file
    ToBeUploadedPath = '/'+ToBeUploaded
    f = open(ToBeUploaded, 'rb')
    response = client.put_file(ToBeUploadedPath, f)

#Rather than crating the entire encryption snippet
#I have used fro the following piece of code from url
#http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

#This function is used to go through all
#the email accounts one by one and then 
#read all the emails. The attachments from 
#all these emails are stripped and syored in 
#temporary location and then either transferred 
#to your dropbox account by encrypting optionally.
def parse_attachments():

    print "(+) Getting all emails for domain jsinix.com"

    for root, subFolders, files in os.walk(vhostdir):
        for file in files:
            all_emails.append(os.path.join(root,file))

    print "(+) Changing PWD to %s" % to_store
    os.chdir(to_store)

    for path in all_emails:
        
        fp = email.parser.FeedParser()
        fp.feed(open(path).read())
        msg = fp.close()

        for msg in msg.walk():
            fname = msg.get_filename()
            if fname == None:
                continue

            try:
	        if os.path.exists(fname) == True:
		    print "(+) Filename %s already exists" % fname
	            continue
	        else:
                    with open(fname, 'wb') as out:
		        print "(+) Writing file %s" % fname
                        out.write(base64.b64decode(msg.get_payload()))
			fname_enc = fname+'.enc'
			fname_final = fname
			if encornot == 1:
			    print "(+) Encrypting %s" % fname
			    encrypt_file(enc_key, fname)
			    fname_final = fname_enc
			print "(+) Uploading %s to dropbox" % fname_final
			jsinix_dropbox_uploader(fname_final)
		
            except TypeError:
                with open(fname, 'wb') as out:
		    print "(+) Error occured for file %s" % fname
		    out.write(message.get_payload())		

def controller():

    print Welcome 
    print "\n\n"
    print Disclaimer	
    parse_attachments()	
    print "(+) Change PWD to %s" % pwd
    os.chdir(pwd)
    print "\n(+) Upload complete"    		

encornot = []

# This script must be run as root to avoid permission
# issues.So lets make sure that no other user can run it.
my_user = getpass.getuser()
if(my_user != 'root'):
    print "(+) Please run this script as ROOT"
    sys.exit()

else:
    os.system("clear")
    if len(sys.argv) == 2:
        if sys.argv[1] == '--encrypt':
	          encornot = 1
	      else:
	          encornot = 0
     else:
	       encornot = 0

    controller()
