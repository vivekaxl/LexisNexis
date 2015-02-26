from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import urlparse
import dbinterface
import json
import os

returnFields = ["first_name_r","last_name_r","headline_r","industry_r","degrees_r","majors_r","colleges_r","skills_r","job_titles_r","companies_r","public_profile_url_r"]
params = ["first_name","last_name","headline","industry","degrees","majors","colleges","skills","job_titles","companies","public_profile_url"]
class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): 
        log = open("log.txt", "a").write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format%args)) 
    ''''first_name_r=on&last_name_r=on&headline_r=on&industry_r=on&degrees_r=on&majors_r=on&colleges_r=on&skills_r=on&job_titles_r=on&companies_r=on&public_profile_url_r=on&count=10&first_name=test&last_name=test&last_name=test&last_name=test&last_name=test&last_name=test&last_name=test&skills=test&job_titles=test&companies=test&public_profile_url=test'''

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path) # get the path
        parsed_query = urlparse.parse_qs(parsed_path.query)
        self.requestHandlers(parsed_path.path, parsed_query)
        return

    def requestHandlers(self, parsedURL, parsedQuery):
        if parsedURL != '/':
            self.render(404, '404')
        elif len(parsedQuery) == 0:
            self.render(200, 'index')
        else:
            self.handleQuery(parsedQuery)

    def render(self, code, path):
        html = open(path+'.html', 'r')
        page = html.read()
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(page)
        return

    def handleQuery(self, query):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        returnDict = dict()
        numberOfProfiles = 'all'
        paramDict = dict()
        for key, value in query.items():
            if type(value) == list and len(value) == 1:
                query[key] = value[0]
            if key in returnFields and query[key] == 'true':
                returnDict[key] = query[key]
            elif key == 'count':
                numberOfProfiles = query[key]
            elif key in params:
                paramDict[key] = query[key].lower()
        if len(paramDict) > 0 and len(returnDict) > 0:
            for param in paramDict.keys():
                paramDict[param] = paramDict[param].split(',')
                for value in xrange(len(paramDict[param])):
                    paramDict[param][value] = paramDict[param][value].strip()
            resultlist = dbinterface.queryer(paramDict)
            finalresult = list()
            for result in resultlist:
                resultDict = dict()
                for key, value in result.items():
                    if key+'_r' in returnDict.keys():
                        if type(value) == str:
                            resultDict[key] = value.title()
                        else:
                            resultDict[key] = value
                finalresult.append(resultDict)
            if numberOfProfiles == 'all':
                numberOfProfiles = len(finalresult)
            else:
                numberOfProfiles = int(numberOfProfiles)
            if len(resultlist) == 1 and resultlist[0].get('error', False):
                self.wfile.write(json.dumps(resultlist))
            else:
                self.wfile.write(json.dumps(finalresult[:numberOfProfiles]))
        elif len(paramDict) == 0:
            self.wfile.write(json.dumps([{'Error':'Please provide at least one parameter to query against'}]))
        elif len(returnDict) == 0:
            self.wfile.write(json.dumps([{'Error':'Please provide at least one field so that we can display the results you require'}]))
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

if __name__ == '__main__':
    server = ThreadedHTTPServer(('', 8080), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Exiting server'
