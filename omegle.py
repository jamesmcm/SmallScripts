#TODO: Make window clearing retain last n lines, make backspace work, separate networking and windowing into different modules, make browsable history
from threading import Thread
from time import sleep
import curses
import urllib2
import curses.textpad


keepGoing=True
newinput=False
#initialize screen
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
termsize=stdscr.getmaxyx()
textwin=curses.newwin(1,termsize[1],termsize[0]-1,0)
stdscr.hline(termsize[0]-2,0,"-",termsize[1])
cury=0
mymsg=""
strangerid=""

#get stranger id
def startChat():
	clearScreen()
	startcon=urllib2.urlopen("http://omegle.com/start", "")
	strangerid=(startcon.read()).replace('"', "")
	return strangerid
def printHelp():
	writeToScreen("Enter the following commands for the described function")
	writeToScreen("OMG_START :starts a chat with a new stranger.")
	writeToScreen("(Please use OMG_DISCONNECT first if in a chat, for good manners :P).")
	writeToScreen("OMG_DISCONNECT :sends a disconnect message to the current stranger.")
	writeToScreen("OMG_CLEAR :clears the message screen. (It is cleared automatically if it fills the window and on new chats.)")
	writeToScreen("OMG_QUIT :Disconencts from the current chat and terminates this application.")
	writeToScreen("OMG_HELP :Prints this help message.")
def writeToScreen(msg):
	global cury
	stdscr.addstr(cury, 0, msg)
	cury+=1
	if cury==termsize[0]-2:
		clearScreen()
	refreshScreen()

def clearScreen():
	global cury
	stdscr.erase()
	cury=0
	refreshScreen()
	
def refreshScreen():
	stdscr.hline(termsize[0]-2,0,"-",termsize[1])
	stdscr.refresh()
	textwin.overwrite(stdscr)
	textwin.redrawwin()
	textwin.refresh()

def sendMsg(msg, strangerid):
	urllib2.urlopen("http://omegle.com/send", "msg="+msg+"&id="+strangerid)

def disconnect(strangerid):
	urllib2.urlopen("http://omegle.com/disconnect", "id="+strangerid)
	


class printinput(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.mymsg=""
		self.newinput=False
	def run(self):
		global keepGoing
		global strangerid
		isCode=False
		while keepGoing:
			mytext.edit()
			self.mymsg=mytext.gather()
			if self.mymsg.find("OMG_QUIT")!=-1:
				keepGoing=False
				isCode=True
			if self.mymsg.find("OMG_DISCONNECT")!=-1:
				disconnect(strangerid)
				isCode=True
			if self.mymsg.find("OMG_START")!=-1:
				strangerid=startChat()
				isCode=True
			if self.mymsg.find("OMG_CLEAR")!=-1:
				clearScreen()
				isCode=True
			if self.mymsg.find("OMG_HELP")!=-1:
				printHelp()
				isCode=True
			if self.mymsg.strip()!="" and isCode==False: #check there is more than just whitespace
				self.newinput=True
				writeToScreen("You: " + self.mymsg)
			isCode=False
			textwin.clear()
			textwin.refresh()

class getevents(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		global keepGoing
		global strangerid
		while keepGoing:
			eventcon=urllib2.urlopen("http://omegle.com/events", "id="+strangerid)
			readevent=eventcon.read()
			start=0
			if readevent.find('["connected"]')!=-1:
				writeToScreen("Stranger connected.")
			if readevent.find('"strangerDisconnected"')!=-1:
				writeToScreen("Stranger Disconnected.")
				writeToScreen("Use OMG_START to restart.")
				#keepGoing=False
			for i in range(readevent.count('"gotMessage"')):
				start=readevent.find('"gotMessage"', start)+15
				theirmsg=readevent[start:readevent.find('"]', start)]
				writeToScreen("Stranger: " + theirmsg)

mytext=curses.textpad.Textbox(textwin)

writeToScreen("Use OMG_START to start a chat and OMG_QUIT to exit, OMG_HELP will print more information. Use Ctrl+h for backspace.")

textThread = printinput()
textThread.start()
eventThread=getevents()
eventThread.start()

#input network stuff should be in main as it is laggy
while keepGoing==True:
	if textThread.newinput==True:
		sendMsg(textThread.mymsg, strangerid)
		textThread.newinput=False

disconnect(strangerid)
textThread.join()
eventThread.join()	
curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()
