#!/usr/bin/python
#TCP server program
import sys
from socket import *
from threading import Thread
from datetime import datetime
import argparse
import os
sys.path.append(os.getcwd()[:os.getcwd().rfind('/')]) # Hack to allow importing databasengine which is
import databasengine as db                            # in parent directory
logger = open('log.txt','a',1)                        # Open in write mode with line buffering

def processQuery(qstring, clientSocket):
    try:
        resultset = db.query.querystring(qstring, db.database) # Call the method in query.py
        if len(resultset) > 0:
            for result in resultset:                     # Print the obtained results (which is in a list)
                for field in result:
                    if type(result[field]) == str:
                        clientSocket.send('\n'+ field + ' : ' + result[field])
                    elif type(result[field]) == list:
                        clientSocket.send('\n'+ field)
                        for element in result[field]:
                            clientSocket.send('\n\t* '+element)
                clientSocket.send('\n'+'='*77+'\n')
        else:
            clientSocket.send("No match found")
    except Exception as e:
        clientSocket.send("Syntax Error in the entered Query, please check your syntax\n"+e.message)

def handleClient(clientSocket, clientAddr):
    clientSocket.send(db.query.__doc__)
    while True:
        try:
            clientSocket.send("\nQuerySQL>")
            qstmt = clientSocket.recv(4096)
            if qstmt.strip() == 'quit':
                clientSocket.send("Closing connection...")
                break
            else:
                print "Received from ", clientAddr, ":: Query: \"", qstmt, "\":: At time", datetime.now() #LOG
                logger.write(datetime.now().ctime()+" Received from "+ clientAddr.__str__()+ " :: Query: \""+ qstmt+ "\""+'\n')
            processQuery(qstmt,clientSocket)
        except error, message:
            print message #LOG
            if message.__str__() != "[Errno 32] Broken pipe":
                logger.write(datetime.now().ctime()+' '+message.__str__()+'\n')
            break
        except KeyboardInterrupt:
            break
    try:
        clientSocket.shutdown(SHUT_RDWR)
        clientSocket.close()
    except error, message:
        pass # assuming that the client has closed already
    print "Client",clientAddr,"closed its connection at",datetime.now() #LOG
    logger.write(datetime.now().ctime()+" Client "+clientAddr.__str__()+" closed its connection"+'\n')

def acceptCLArguments():
    # Initializing parser for accepting command line arguements
    parser = argparse.ArgumentParser(
        description="""TCP server layer to the database engine. This is a testing module""")

    # Assign port number to socket
    parser.add_argument(
        '-p','--port', default=12000, type=int, metavar='int',
        help='The port where the server should run (integer > 1024 and < 65535) Default: 12000')

    # Number of profiles to generate
    parser.add_argument(
        '-n','--number', default=10000, type=int, metavar='int',
        help='Number of profiles to generate at the start of the server')

    return parser.parse_args()

def initserver(number):
    logger.write(datetime.now().ctime()+' Booting up the server'+'\n')
    for name, details in db.generator.generate(number).items():
        db.create(name, details)

def allocateResources(port):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)  #Socket to interact with the client 
        clientSocket.bind(('', int(port)))
        clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        clientSocket.listen(5);
    except error, message:
        print message
        logger.write(datetime.now().ctime()+' '+message.__str__()+'\n')
        if message.__str__() == "[Errno 98] Address already in use":
            print 'Please try booting the server with a different port'
            sys.exit(0)
        return None
    return clientSocket

def acceptClient(clientSocket):
    while clientSocket:
        connSocket, clientAddr = clientSocket.accept()
        print 'Connected to client',clientAddr,"at time",datetime.now()
        logger.write(datetime.now().ctime()+" Client "+clientAddr.__str__()+" opened its connection"+'\n')
        t= Thread(target=handleClient, args=(connSocket, clientAddr))
        t.start()

if __name__ == '__main__':
    args = acceptCLArguments()
    initserver(args.number)
    print 'Completed initialization. Ready to accept clients'
    try:
        acceptClient(allocateResources(args.port))
    except KeyboardInterrupt:
        print 'Exiting server'
        logger.write(datetime.now().ctime()+' Closed server')
        sys.exit(0)