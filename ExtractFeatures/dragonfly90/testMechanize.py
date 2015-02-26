import mechanize
br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_equiv(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
page = br.open("http://www.google.com/")
htmlcontent = page.read()
print htmlcontent
print br.title()

for f in br.forms():
    print f
