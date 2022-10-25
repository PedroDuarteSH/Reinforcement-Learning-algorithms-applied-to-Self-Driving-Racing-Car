
import socket
import sys
import os

import subprocess
import signal
from torcs_env.envs.msgParser import MsgParser

BUFFER_SIZE = 1024
uppath = lambda _path, n: os.sep.join(_path.split(os.sep)[:-n])
TORCS_PATH = uppath(__file__, 3) + '\\torcs'




class TorcsClient:
    def __init__(self, training = False):
        
        self.messageParser = MsgParser()
        
        self.host = 'localhost'
        self.port = 3001
        self.bot_id = 'SCR'
        
        self.sock = self.init_socket()
        
        self.training = training
        self.process = None
        self.start_race()
        self.connect()
    
    
    def init_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
            print ('Could not make a socket.')
            sys.exit(-1)

        # one second timeout
        sock.settimeout(1.0)
        return sock
                

    def start_race(self):
        if self.training:
            self.process = subprocess.Popen(["wtorcs.exe",  "-r", "race_config.xml"], cwd=TORCS_PATH, )
        else:
            self.process = subprocess.Popen(["wtorcs.exe"], cwd=TORCS_PATH, )
    
    def kill(self):
       # os.kill(self.process.pid, signal.CTRL_C_EVENT)
        self.sock.close()

    def init(self):
        '''Return init string with rangefinder angles'''
        self.angles = [0 for x in range(19)]
        
        for i in range(5):
            self.angles[i] = -90 + i * 15
            self.angles[18 - i] = 90 - i * 15
        
        for i in range(5, 9):
            self.angles[i] = -20 + (i-5) * 5
            self.angles[18 - i] = 20 - (i-5) * 5
        
        return self.messageParser.stringify({'init': self.angles})

        
    def connect(self):
        while True:
            buf = self.bot_id + self.init()
            #print ('Sending init string to server:', buf)
    
            try:
                self.sock.sendto(buf.encode(), (self.host, self.port))
            except socket.error:
                print ("Failed to send data...Exiting...")
                sys.exit(-1)
                
            try:
                buf, addr = self.sock.recvfrom(BUFFER_SIZE)
                if buf.decode().find('***identified***') >= 0:
                    print ('Received: ', buf)
                    return
            except socket.error:
                ...
                #print ("didn't get response from server...")
    
    
    def sendMessage(self, message):
        try:
            buf = self.messageParser.stringify(message)
            self.sock.sendto(buf.encode(), (self.host, self.port))
            return
        except socket.error:
            print ("Failed to send data...Exiting...")
            sys.exit(-1)
            
            
    def recieveMessage(self):
        while(True):
            buf = None
            try:
                buf, _ = self.sock.recvfrom(BUFFER_SIZE)
                if(buf != None):

                    return self.messageParser.parse(buf.decode())
                return buf.decode()
            except socket.error:
                print ("didn't get response from server...")
            
    


    

    
