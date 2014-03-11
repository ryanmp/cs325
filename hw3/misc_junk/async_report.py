import asyncore
import socket
import json
import signal
import threading
import time
import os
import sys

if len(sys.argv) < 2:
	print 'You must specify an IP to connect to to monitor!'
	print 'like so:  reporty.py 127.0.0.1'
	sys.exit(1)

SHUTDOWN = False
if len(sys.argv) == 3:
	if '-k' in sys.argv[2] :
		print 'Shutting down Server in Three Seconds...'
		SHUTDOWN = True
	else:
		print 'Not sure what that argument was.'

#change these values only
HOST = sys.argv[1]   # The remote host
PORT = 2541          # The same port as used by the server. Default 2541
#change these values only

#Global variables
serverFound = []
serverClients = []
serverNumber = 0
t1 = 0
t2 = 0
n1 = 0
n2 = 0

#Function used for clearing screen
clear = lambda: os.system('cls')

#deal with signals
#Shutdown all threads as well
def signal_handler(signum, frame):
	if signum == 2:
		signum = 'Control-c'
	print 'SHUTDOWN!  Reason:', signum
	report.t.stop()
	time.sleep(1)
	sys.exit()

#yup, server is still there!
def dealKeepAlive(self, payload):
	print 'got keep-alive back from server!'

def dealReportFound(self, serverFoundParam):
	global serverFound
	serverFound = serverFoundParam

def dealReportClients(self, serverClientsParam):
	global serverClients
	serverClients = serverClientsParam

def dealReportNumber(self, num):
	global serverNumber
	serverNumber = num
	
def dealServerShutdown(self, reason):
	time.sleep(2)
	clear()
	print ''
	print 'The Server Has Shutdown.  Total Stats:'
	print ''
	print 'Server Found', len(serverFound), 'perfect numbers:'
	print serverFound
	print 'Server Checked Numbers up to:', serverNumber
	print ''
	print 'We monitored the server for:', int (t2 - t1), 'seconds'
	print 'Numbers chicked during that time:', int (n2 - n1)
	print 'Numbers Checked Per Second:', int( int(n2-n1) / int(t2-t1) )

#main class which handles the async part of the client.
#It then calls out, and starts up the actuall processing thread
class AsyncReport(asyncore.dispatcher):
	buffer = ""
	t = None

	def __init__(self, host):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( (host, PORT) )
		self.t = CursesThread(self)
		self.t.start()

	#adds the requested json to the send buffer
	def sendJson(self, id, payload):
		self.send ( json.dumps( {"id":id, "payload":payload} ) )

	#got the message to kill self
	#Also, make sure we kill the child thread too
	def handle_close(self):
		self.close()
		self.t.stop()

	#Deals with any packets received
	#Delegates them out to be processed
	def handle_read(self):
		jdata = self.recv(8192)
		#print jdata
		#assuming we actually received SOMETHING.....
		if jdata:
			#lets load up that json!  (DOES NOT DEAL WITH INVALID JSON!)
			data = json.loads(jdata)
			if data['id'] == 0:
				lol = data['payload']
				dealKeepAlive(self, lol)
			elif data['id'] == 5:
				foundArray = data['payload']
				dealReportFound(self, foundArray)
			elif data['id'] == 6:
				clientsArray = data['payload']
				dealReportClients(self, clientsArray)
			elif data['id'] == 7:
				numberServer = data['payload']
				dealReportNumber(self, numberServer)
			elif data['id'] == 9:
				reason = data['payload']
				dealServerShutdown(self, reason)
			else:
				print 'something went wrong.'

#Thread that actually does all the processing
class CursesThread(threading.Thread):
	_stop = False

	def __init__(self, report):
		super(CursesThread,self).__init__()
		self.report = report

	#We received the signal to stop from the parent class
	#or from the signal handler.  Stop what we are doing now
	def stop(self):
		self._stop = True

	#What the thread actually does
	def run(self):
		global serverNumber
		global t1
		global t2
		global n1
		global n2
		print 'connecting....'
		
		#initial Setup Queries
		report.sendJson( 7, 'what number are you on?' )
		time.sleep(0.5)
		report.sendJson( 5, 'gimme found numbers.' )
		time.sleep(0.5)
		t1 = time.time()
		n1 = serverNumber
		
		if SHUTDOWN == True:
			report.sendJson( 9, 'this is my password' )
			time.sleep(0.5)
		
		while self._stop == False:
			report.sendJson( 5, 'gimme found numbers.' )
			time.sleep(0.5)
			report.sendJson( 6, 'gimme connection list.' )
			time.sleep(0.5)
			report.sendJson( 7, 'what number are you on?' )
			
			t2 = time.time()
			n2 = serverNumber
			
			#just a safety check to prevent some display bugs
			if self._stop == True:
				sys.exit()
			clear()
			print ''
			print 'Report Thread is now Monitoring'
			print ''
			print ''
			print 'Numbers found:', serverFound
			print ''
			print 'Number of active clients:', len(serverClients)
			print ''
			print 'Currently on:', serverNumber
			print 'Monitoring for:', int (t2 - t1)
			print 'Number since started:', int (n2 - n1)
			print 'Numbers Checked Per Second', int( int(n2-n1) / int(t2-t1) )
			
			time.sleep(1.5)

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#ok, now actually start up the client!
report = AsyncReport(HOST)
asyncore.loop(1)