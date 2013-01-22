#Aim: Connect to two Omegle chats, pass messages from one to other, log all messages.

from threading import Thread
from time import time, sleep, strftime, gmtime
from random import randint
import urllib2
import os
urllib2.install_opener(urllib2.build_opener())
keepGoing=True
alias=""
recvfrom=""
sendto=""
pfile=open("proxylist.txt","r")
proxyfile=pfile.read()
i=0
string=""
proxylist=[]
for char in proxyfile:
    if (char!='\n'):
        string=string+char
    if (char=='\n'):
        proxylist.append(string)
        #print string
        string=""

i=randint(0, len(proxylist)-1)
proxy_handler=urllib2.ProxyHandler({"http": proxylist[i]})
urllib2.install_opener(urllib2.build_opener(proxy_handler))

def newProxy():
    i=randint(0, len(proxylist)-1)
    print("DEBUG: Changing proxy to "+proxylist[i])
    proxy_handler=urllib2.ProxyHandler({"http": proxylist[i]})
    urllib2.install_opener(urllib2.build_opener(proxy_handler))

def filePreparation():
    tempname=time()
    omlogdir=os.path.join(os.curdir, "omlogs")
    flog=open(omlogdir+"/" + str(tempname)+".txt","w") #remember to flog.close() on quit
    return flog
def startChat():
    #try:
    startcon=urllib2.urlopen("http://omegle.com/start", "")
    strangerid=(startcon.read()).replace('"', "")
    #except:
        #newProxy()
        #strangerid="ERROR"
    return strangerid

def logMsg(msg, alias):
    print("["+strftime("%H", gmtime())+":"+strftime("%M", gmtime())+"] "+alias+": "+msg+"\n") #Mainly for debugging purposes, may be removed
    flog.write("["+strftime("%H", gmtime())+":"+strftime("%M", gmtime())+"] "+alias+": "+msg+"\n")

def sendMsg(msg, strangerid):
    urllib2.urlopen("http://omegle.com/send", "msg="+msg+"&id="+strangerid)

def disconnect(strangerid):
    #try:
    urllib2.urlopen("http://omegle.com/disconnect", "id="+strangerid)
    #except:
        #newProxy()
        #disconnect(strangerid)

def quitprogram(strangerA, strangerB):
    #disconnect(strangerA)
    #disconnect(strangerB)
    flog.close()
    Athread.join()
    Bthread.join()
   

class strangerChat(Thread):
    def __init__(self, alias, recvfrom, sendto):
        Thread.__init__(self)
        self.recvfrom=recvfrom
        self.sendto=sendto
        self.alias=alias
    def run(self):
        global keepGoing
        global timer
        while keepGoing:
            eventcon=urllib2.urlopen("http://omegle.com/events", "id="+self.recvfrom)
            readevent=eventcon.read()
            start=0
            if readevent.find('["connected"]')!=-1:
                logMsg(self.alias+" connected.", "SERVER")
            if readevent.find('"strangerDisconnected"')!=-1:
                logMsg(self.alias+" disconnected.", "SERVER")
                #disconnect(self.sendto)
                keepGoing=False
            for i in range(readevent.count('"gotMessage"')):
                start=readevent.find('"gotMessage"', start)+15
                theirmsg=readevent[start:readevent.find('"]', start)]
                logMsg(theirmsg, self.alias)
                sendMsg(theirmsg, self.sendto)
                timer=0
                if theirmsg.find("Please reload the page for technical reasons.")!=-1:
                    #disconnect(self.sendto)
                    newProxy()
                    keepGoing=False


#Initialize


limit=1000
chatnum=0
while(chatnum<limit):
    keepGoing=True
    timer=0
    strangerA="ERROR"
    strangerB="ERROR"
    flog=filePreparation()
    #while(strangerA=="ERROR"):
    strangerA=startChat()
    #while(strangerB=="ERROR"):
    strangerB=startChat()
    Athread=strangerChat("A", strangerA, strangerB)
    Athread.start()
    Bthread=strangerChat("B", strangerB, strangerA)
    Bthread.start()

    while keepGoing:
        sleep(1) #Add timer here later perhaps
        timer=timer+1
        if timer>300:
            keepGoing=False
    quitprogram(strangerA, strangerB)
    chatnum=chatnum+1
