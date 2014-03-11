import asyncore, socket, json, signal, threading
from time import sleep
from sys import stdout, exit

from helpers import *
from algo_greedy import *

#change these values only
DEBUG = True
#change these values only

#Global Variables
derp = []

#Packet Constants#
KEEP_ALIVE = 0  #C -> S #Keep-alive
C_REQ_WORK = 1  #C -> S #Request for work
C_SEND_RES = 2  #C -> S #Rend result
C_REQ_UPDT = 3  #C -> S #Request meta-info update
##Server Packets##
S_SEND_UPD = 10 #S -> C #Send meta-info update
S_SERV_KIL = 11 #S -> C #Server Shutting down
##algorithm Packets##
S_WORK_GRE = 20 #S -> C #Send greedy algorithm work
S_WORK_MST = 21 #S -> C #Send MST algorithm work
##Improvement Packets##
S_IMP_SGMT = 30 #S -> C #Send improvement work, swapping segments
S_IMP_SCTY = 31 #S -> C #Send improvement work, swapping cities

def signal_handler(signum, frame):
	if DEBUG == True:
		client.t.stop()
		exit()
	print "Sorry, I've disabled killing the client using control-c, as It could conceivably cause some data to be lost, if it is done at a very bad time for the server."

def dealGreedyWork(self, payload):
	data = json.loads(payload)
	

#main class which handles the async part of the client.
#It then calls out, and starts up the actual processing thread
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
		if DEBUG:
			print jdata
		#assuming we actually received SOMETHING.....
		if jdata:
			#lets load up that json!  (DOES NOT DEAL WITH INVALID JSON!)
			data = json.loads(jdata)
			if data['id'] == S_SEND_UPD:
				print "We got our meta-info update"
				payload = data['payload']
				#dealMetaInfo(self, payload)
			elif data['id'] == S_SERV_KIL:
				print "Our server is shutting down! :("
				sleep(10)
				exit()
			elif data['id'] == S_WORK_GRE:
				payload = data['payload']
				dealGreedyWork(self, payload)
				#Server sent us some greedy algo work
			elif data['id'] == S_WORK_MST:
				payload = data['payload']
				dealMSTWork(self, payload)
				#Server sent us some MST algo work
			elif data['id'] == S_IMP_SGMT:
				payload = data['payload']
				dealImproveSegment(self, payload)
				#Server sent us some segment swapping improvement work
			elif data['id'] == S_IMP_SCTY:
				payload = data['payload']
				dealImproveCity(self, payload)
				#Server sent us some city swapping improvement work
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
		if (self._stop == True):
			exit()
		#self.client.sendJson(C_REQ_WORK, 'client connecting...')
		#sleep(5)
		self.client.sendJson(0, 'client connecting...')
		sleep(1)
		self.run()

#Initialize by asking for remote host info
HOST = raw_input("Server IP? (Defaults to localhost): ")
if (HOST == ''):
	HOST = '127.0.0.1'
PORT = raw_input("Server Port? (Defaults to 31337): ")	#Default 31337
if (PORT == ''):
	PORT = 31337

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#ok, now actually start up the client!
client = AsyncClient(HOST)
asyncore.loop(1)