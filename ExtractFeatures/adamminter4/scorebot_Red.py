#! /usr/bin/env python

"""
A simple echo server for Red Team to connect to for scoring.
"""

import socket
import time

class RedServer:
    def _init_(self):
        self.HOST = socket.AF_INET
        self.PORT = 50000
        self.BUFFERSIZE = 1024
        self.ADDRESS = (self.HOST,self.PORT)
        self.collectionOfCallbacks = []
        self.COMPETITION_CLOCK = time.time();
        self.roundNumber = 0
        self.pointTotal = 0
        self.running = True
        self.serverSock = socket.socket()
        self.serverSock.bind(self.ADDRESS)
        self.serverSock.listen(5)
        self.windowOpen = true
        print("Waiting for callbacks...")
        while self.running:
            if self.windowOpen:
                #clientInfo[0] is information about the client
                #clientInfo[1] is the address the connection came from
                clientInfo = self.serverSock.accept()
                data = clientInfo[0].recv(size)
                
                #If we actually get anything from the connection, send it right back!.
                if data:
                    print("Callback connected from {}.".format(clientInfo[1]))
                    clientInfo[0].send(data)
                    if self.collectionOfCallbacks.count(clientInfo[1]) == 0:
                        self.collectionOfCallbacks.append(clientInfo[1])
                    else:
                        print("Callback already logged from {}.".format(clientInfo[1]))
                
                #If at the end of a round; Rounds last 10 minutes.
                if (time.time() - self.COMPETITION_CLOCK) == 10:
                    #Reset the competition clock to the current time and update the round.
                    print("Window for callbacks closed.")
                    self.windowOpen = false
                
            else:
                self.roundNumber++
                print("Competing the scoring for round {}.", self.roundNumber)
                scoreRed()
                print("Resetting the game clock for round {} and reopening the window for callbacks.", self.roundNumber + 1)
                self.COMPETITION_CLOCK = time.time();
                
                #Need to reset the array of any callbacks for the next round.
                self.collectionOfCallbacks = []
                windowOpen = true
                
        self.serverSock.close()
        print("- end -")

    def scoreRed():
        points = 0
        f = open('redscore.txt', 'w')
        print("Writing score to file.")
        
        f.write("-------------------Round " + self.roundNumber + "-----------------------");
        f.write("Red Team called the Gold Team from the following ip ranges: \n")
        for ip in self.collectionOfCallbacks:
            f.write(.format(ip) + "\n")
            points++
        self.pointTotal = self.pointTotal + points
        f.write("Red Team scored " + points + " point(s) for this round. \n")
        f.write("The Red Team has scored a total of " + self.pointTotal + " points so far\n");
        f.write("-------------------End Round " + self.roundNumber + "-------------------\n\n\n")
        f.close()
        
        print("Scoring complete.")

srvr = redServer()
