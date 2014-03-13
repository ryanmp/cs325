import asyncore, asynchat, socket, threading
import signal, pickle, sys, os
from time import sleep
from sys import stdout, exit

from helpers import *
from algo_greedy import *
from algo_mst import *
from algo_inverse_prim import *
from algo_improve_rev import *
from algo_improve_swap import *

#change these values only
DEBUG = True	# 3= show all packet data.
#change these values only

#Global Variables
shortest = sys.maxint
cities = []
route = []
mode = ""
curGreedy = ""
clients = []

#Packet Constants#
KEEP_ALIVE = 0  #C -> S #Keep-alive
C_REQ_WORK = 1  #C -> S #Request for work
C_SEND_RES = 2  #C -> S #Rend result
C_REQ_UPDT = 5  #C -> S #Request meta-info update
##Server Packets##
S_SEND_UPD = 10 #S -> C #Send meta-info update
S_SERV_KIL = 11 #S -> C #Server Shutting down
##algorithm Packets##
S_WORK_GRE = 20 #S -> C #Send greedy algorithm work
S_WORK_MST = 21 #S -> C #Send MST algorithm work
S_WORK_PRM = 22 #S -> C #Send Reverse Prim algorithm work
##Improvement Packets##
S_IMP_SGMT = 30 #S -> C #Send improvement work, swapping segments
S_IMP_SCTY = 31 #S -> C #Send improvement work, swapping cities
##Monitor / Control Packets##
M_GET_CURR = 40 #M -> S #Request current status
M_SET_MODE = 43 #M -> S #Request server mode change
##Server (monitor) Reply Packets##
S_SEND_STA = 50 #S -> M #Respond with current status

def signal_handler(signum, frame):
	print "Closing socket..."
	sleep(2)
	client.t.stop()
	sleep(2)
	exit()

def clear():
	os.system('cls')
	os.system('clear')

def dealMetaInfoUpdate(self, payload):
	global shortest, cities, route
	shortest, cities, route = pickle.loads(payload)

def dealStatusUpdate(self, payload):
	global mode, clients, curGreedy
	curGreedy, mode, clients = pickle.loads(payload)

#main class which handles the async part of the client.
#It then calls out, and starts one of these up for incoming packets
class AsyncClient(asynchat.async_chat):
	buffer = ""
	t = None

	def __init__(self, host):
		asynchat.async_chat.__init__(self)
		self.set_terminator("\r\n\r\n")
		self.request = None
		self.data = ""
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( (host, PORT) )
		self.t = SenderThread(self)
		self.t.start()

	def collect_incoming_data(self, data):
		self.data = self.data + data

	def found_terminator(self):
		data = self.data
		self.data = ""
		#lets load up that pickle!  (DOES NOT DEAL WITH INVALID PICKLE!)
		id, payload = pickle.loads(data)
		#Assuming we actually received SOMETHING.....
		if data:
			if (DEBUG == 3):
				print id, payload
			if id == S_SERV_KIL:
				print "Our server is shutting down! :("
				sleep(10)
				exit()
			elif id == S_SEND_UPD:
				dealMetaInfoUpdate(self, payload)
				#Server sent Info.  Update local copy.
			elif id == S_SEND_STA:
				dealStatusUpdate(self, payload)
				#Server sent us a status info update
			else:
				print 'Something went wrong.', id, payload

	#Adds the requested pickle to the send buffer
	def sendPickle(self, id, payload):
		self.push(pickle.dumps([id, payload]) + "\r\n\r\n")

	#Got the message to kill self
	#Also, make sure we kill the child thread too
	def handle_close(self):
		print "Server not reachable.  Saving best list to pickle to be safe."
		pickle.dump(route, open('backup.p', 'wb'))
		self.close()
		self.t.stop()

#Thread that actually does all the processing
class SenderThread(threading.Thread):
	_stop = False

	def __init__(self, client):
		super(SenderThread,self).__init__()
		self.client = client

	#We received the signal to stop from the parent class
	#Or from the signal handler.  Stop what we are doing now
	def stop(self):
		self._stop = True

	#What the thread actually does
	def run(self):
		while (self._stop == False):
			self.client.sendPickle(C_REQ_UPDT, 'M update')
			sleep(1)
			self.client.sendPickle(M_GET_CURR, 'M Status')
			sleep(1)
			clear()
			print "\n\n\ncurrent best:", shortest
			print "\n#of cities:", len(cities), "#Cities in result:", len(route)
			print "\n#of active clients:", len(clients)
			print "current Greedy level:", curGreedy
			print "\n\nmode:", mode
			sleep(10)

#Initialize by asking for remote host info
clear()
HOST = raw_input("Server IP? (Defaults to localhost): ")
if (HOST == ''):
	HOST = '127.0.0.1'
PORT = raw_input("Server Port? (Defaults to 31337): ")
if (PORT == ''):
	PORT = 31337

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#ok, now actually start up the client!
client = AsyncClient(HOST)
asyncore.loop(1)