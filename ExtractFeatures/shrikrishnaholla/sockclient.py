#!/usr/bin/python
#TCP client program
from socket import *
import argparse
import sys

def acceptCLArguments():
    # Initializing parser for accepting command line arguements
    parser = argparse.ArgumentParser(
        description="""TCP client to the server. This is a testing module""")

    # IP address where the server is running
    parser.add_argument(
        '-ip','--serverip', default="localhost", type=str, metavar='str',
        help='The hostname/ip of the server. Default: localhost')

    # Assign port number to socket
    parser.add_argument(
        '-p','--port', default=12000, type=int, metavar='int',
        help='The port where the server is running (integer > 1024 and < 65535) Default: 12000')

    return parser.parse_args()

def transact(host,port):
    try:
        serversocket = socket(AF_INET,SOCK_STREAM)
        serversocket.settimeout(5.0)
        serversocket.connect((host,port))
        serversocket.settimeout(None)
    except error, message:
        print message
        sys.exit(0)

    while True:
        try:
            while True:                            # Loop till all the data that server has to send,
                data = serversocket.recv(4096)     # is received
                print data
                if data.find('QuerySQL>') != -1:   # Server sends this string once all results have been
                    break                          # printed
                if data.find('Closing') != -1:
                    raise KeyboardInterrupt
            serversocket.send(raw_input(''))
        except error, message:
            print message
            break

        except KeyboardInterrupt:
            print 'Exiting client...'
            serversocket.shutdown(SHUT_RDWR)
            serversocket.close()
            break

if __name__ == '__main__':
    args = acceptCLArguments()
    transact(args.serverip, args.port)