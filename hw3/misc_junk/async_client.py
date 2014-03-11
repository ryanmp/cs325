import asyncore
import socket
import json
import signal
import threading
import time
import sys
from random import randrange

if len(sys.argv) != 2:
	print 'You must specify an IP to connect to to monitor!'
	print 'like so:  client.py 127.0.0.1'
	sys.exit(1)

#change these values only
HOST = sys.argv[1]   # The remote host
PORT = 2541          # The same port as used by the server. Default 2541
#change these values only

each = 0
currNum = 0

#deal with signals
#Shutdown all threads as well
def signal_handler(signum, frame):
	if signum == 2:
		signum = 'Control-c'
	print 'SHUTDOWN!  Reason:', signum
	client.t.stop()
	time.sleep(1)
	sys.exit()

#We found a perfect number!
#Send it off the the server.
def dealFoundPerfect(self, num):
	print 'found perfect number.  sending', num, 'to server.'
	client.sendJson(3, num)
	time.sleep(1)

#yup, server is still there!
def dealKeepAlive(self, payload):
	print 'got keep-alive back from server!'

#Find perfect numbers from min to min+each
#disable, if True, will prevent it from sending found numbers tot he server
def findPerfectNumbers(self, min, disable):
	global each
	n = min
	max = min+each
	while n < max:
		factors = [1]
		[factors.append(i) for i in range(2,n+1) if n%i == 0]
		if sum(factors) == 2*n:
			if disable != 'True':
				dealFoundPerfect(self, n)
		n += 1

#loops through, calculating how many perfect numbers your computer can find in 15 seconds.
#it checks how many you can numbers near 100,000 your computer can check in 15 seconds
def calcSpeed(self):
	global each
	print 'we are now checking how fast your computer is.'
	print 'This should take exactly 15 seconds...'
	t1 = time.time()
	t2 = time.time()
	while t2 - t1 < 15:
		findPerfectNumbers('derp', 100000, 'True')
		t2 = time.time()
		each += 1
	each = (each * 3)
	print 'your computer will do', each, 'numbers at a time.'

#main class which handles the async part of the client.
#It then calls out, and starts up the actuall processing thread
class AsyncClient(asyncore.dispatcher):
	buffer = ""
	t = None

	def __init__(self, host):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( (host, PORT) )
		self.t = SenderThread(self)
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
			elif data['id'] == 2:
				beginning = data['payload']
				self.t.dealRangeAggignment(beginning)
			elif data['id'] == 9:
				reason = data['payload']
				signal_handler(reason, 2)
			else:
				print 'something went wrong.'

#Thread that actually does all the processing
class SenderThread(threading.Thread):
	_stop = False

	def __init__(self, client):
		super(SenderThread,self).__init__()
		self.client = client

	#We received the signal to stop from the parent class
	#or from the signal handler.  Stop what we are doing now
	def stop(self):
		self._stop = True

	#What the thread actually does
	def run(self):
		global each
		self.client.sendJson(1, each)
	
	#called when we receive an assignment of a range of numbers from the server
	def dealRangeAggignment(self, beginning):
		global currNum
		global each
		currNum = beginning
		print 'now fiding perfect numbers between', beginning, 'and', beginning+each
		t1 = time.time()
		findPerfectNumbers(self, beginning, 'false')
		t2 = time.time()
		#this is optional, but makes the amount the client asks for adaptive.
		#That is, as numbers get harder to compute, Each client will do less at a time.
		if t2-t1 < 10:
			each += 5
		elif t2-t1 > 20:
			each -= 5
		#This actually requests more
		self.run()

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#calculate our speed.....
calcSpeed('derp')

#ok, now actually start up the client!
client = AsyncClient(HOST)
asyncore.loop(1)