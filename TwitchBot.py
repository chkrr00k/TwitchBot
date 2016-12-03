import sys
import socket
import string
import ssl
import threading
import time

NICK = "NICK"
PASS = "oauth:OAUTH"

##MODEL
class Server:
    #private sock
    #private stringBuffer
    def __init__(self, server, port=6667, sslU=False):
        self.sock = socket.socket( )
        if sslU:
            self.sock = ssl.wrap_socket(self.sock)
        self.sock.connect((server, port))
        self.stringBuffer = ""
        
    def write(self, message):
        self.sock.send(bytes(message, "UTF-8"))
        time.sleep(0.2)
    
    def read(self):
        #old string + string just read.
        self.stringBuffer = self.stringBuffer + self.sock.recv(1024).decode("UTF-8")
        #split the string in corrispondence of "\n" to have a list of message ("\r" is still there)
        tmp = self.stringBuffer.split("\n")
        #
        self.stringBuffer = tmp.pop()
        return tmp
    
class Irc:
    #private ServerObj
    def __init__(self, server, port=6667, sslU=False):
        self.ServerObj = Server(server, port, sslU);
        self.lastString = ""
        self.messages = []
    
    def pingHandler(self, line):
        self.ServerObj.write("PONG " + (line.split() [1]) + "\r\n")

    def messageHandler(self, line):
        tokLine = line.split()
        nickName = ((tokLine[0]).split("!")[0]).strip()[1:]
        channel = (tokLine[2]).strip()
        message = line.split(" :")[1]
        return nickName, channel, message
    
    def sendMessage(self, channel, message):
        self.ServerObj.write("PRIVMSG " + channel + " :" + message +"\r\n")

    def readline(self):
        return self.ServerObj.read()

    def joinChannel(self, channel):
        self.ServerObj.write("JOIN " + channel + "\r\n")
        
    def connect(self):
        self.ServerObj.write("PASS " + PASS + "\r\n")
        self.ServerObj.write("NICK " + NICK + "\r\n")

## define spambot behaviour here
class Spammer(threading.Thread):
    def __init__(self, twitch):
        threading.Thread.__init__(self)
        self.twitch = twitch
    
    def run(self):
        while 1:
            twitch.sendMessage("#CHANNELTOSEND", "MESSAGE")
            time.sleep(1)

##CONTROLLER

twitch = Irc("irc.chat.twitch.tv")
print("connecting")
twitch.connect()
time.sleep(0.5)
spa = Spammer(twitch)
auth = False
while 1:
    msgList = twitch.readline()
    for msg in msgList:
        if msg.startswith("PING"):
            irc.pingHandler(msg.rstrip())
            print("PONGED")
            
        if msg.find("004") and not auth:
            spa.start()
            auth = True
        print(msg)

 
