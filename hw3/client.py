import asyncore, asynchat, socket, threading
import signal, pickle, sys, os
from time import sleep
from sys import stdout, exit

from helpers import *
from algo_greedy import *
from algo_mst import *
from algo_improve_rev import *
from algo_improve_swap import *
from algo_improve_rev_wrap import *

#change these values only
DEBUG = True	# 3= show all packet data.
#change these values only

#Global Variables
shortest = sys.maxint	#The length of the current shortest route
cities = []		#The list of all cities
route = []		#Our current route of cities that we are operating on
working = False		#Are we currently working?

#####PACKETS#####
##Client Packets##
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
S_IMP_SGT2 = 32 #S -> C #Send Improvement Work, swapping segments with wraparound

#deal with signals
def signal_handler(signum, frame):
	print "Closing socket..."
	client.t.stop()
	sleep(2)
	exit()

#Handles doing a run of greedy
def dealGreedyWork(self, _start):
	global working, shortest, route
	working = True
	if DEBUG:
		print "now doing greedy for: ", _start
	result = algo_greedy_start(cities, _start)
	length = route_length_final(cities, result)
	if (shortest > length):
		print "Found a shorter route.  Updating local cache, and sending route to server."
		shortest = length
		route = result[0:]
		self.sendPickle(C_SEND_RES, result)
	working = False

#Handles doing a run of MST routing
def dealMSTWork(self, payload):
	global working
	working = True
	if DEBUG:
		print "now calculating MST TSP."
	result = algo_mst(cities)
	working = False
	self.sendPickle(C_SEND_RES, result)

#Handles doing a run of prim's algorithm.
def dealPrimWork(self, payload):
	global working
	working = True
	if DEBUG:
		print "now calculating MST TSP."
	result = algo_inverse_prim(cities)
	working = False
	self.sendPickle(C_SEND_RES, result)

#Handles running a set of segment swap
def dealImproveSegment(self, payload):
	global route, shortest, working
	working = True
	start_length, end_length, route = pickle.loads(payload)
	for i in xrange(start_length, end_length):
		if DEBUG:
			print "Running segment swap, length:", i
		new_route = algo_improve_rev(cities, route, i)
		len_old = route_length_final(cities, route)
		len_new = route_length_final(cities, new_route)
		if (len_old > len_new):
			print "Segment swap has improved:", len_old, ">", len_new
			route = new_route[0:]
			shortest = len_new
	self.sendPickle(C_SEND_RES, new_route)
	working = False

#Handles running a set of Wrapping segment swap
def dealImproveSegment2(self, payload):
	global route, shortest, working
	working = True
	start_length, route = pickle.loads(payload)
	if DEBUG:
		print "Running segment swap, length:", start_length
	new_route = algo_improve_rev_wrapper(cities, route, start_length)
	len_old = route_length_final(cities, route)
	len_new = route_length_final(cities, new_route)
	if (len_old > len_new):
		print "Segment swap has improved:", len_old, ">", len_new
		route = new_route[0:]
		shortest = len_new
		self.sendPickle(C_SEND_RES, new_route)
	working = False

#Handles running city swap on a specified city
def dealImproveCity(self, payload):
	global route, shortest, working
	working = True
	start_city, route = pickle.loads(payload)
	if DEBUG:
		print "Running city swap, city:", start_city
	new_route = algo_improve_swap(cities, route, start_city)
	len_old = route_length_final(cities, route)
	len_new = route_length_final(cities, new_route)
	if (len_old > len_new):
		print "City swap has improved:", len_old, ">", len_new
		route = new_route[0:]
		shortest = len_new
		self.sendPickle(C_SEND_RES, new_route)
	working = False

#Handles updating local meta info.
def dealMetaInfoUpdate(self, payload):
	global shortest, cities, route
	shortest, cities, route = pickle.loads(payload)
	if DEBUG:
		print  "#Cities:", len(cities), "Shortest so far:", shortest, "#Cities in route:", len(route)

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
			if id == S_SEND_UPD:
				dealMetaInfoUpdate(self, payload)
				#Server sent Info.  Update local copy.
			elif id == KEEP_ALIVE:
				print "connected, but idle."
			elif id == S_SERV_KIL:
				print "Our server is shutting down! :("
				sleep(10)
				exit()
			elif id == S_WORK_GRE:
				dealGreedyWork(self, payload)
				#Server sent us some greedy algo work
			elif id == S_WORK_MST:
				dealMSTWork(self, payload)
				#Server sent us some MST algo work
			elif id == S_WORK_PRM:
				dealPrimWork(self, payload)
				#Server sent us some reverse prim algo work
			elif id == S_IMP_SGMT:
				dealImproveSegment(self, payload)
				#Server sent us some segment swapping improvement work
			elif id == S_IMP_SGT2:
				dealImproveSegment2(self, payload)
				#Server sent us some segment swapping improvement work with wraparound
			elif id == S_IMP_SCTY:
				dealImproveCity(self, payload)
				#Server sent us some city swapping improvement work
			else:
				print 'Something went wrong.', id, payload

	#Adds the requested pickle to the send buffer
	def sendPickle(self, id, payload):
		self.push(pickle.dumps([id, payload]) + "\r\n\r\n")

	#Got the message to kill self
	#Also, make sure we kill the child thread too
	def handle_close(self):
		global cities, route
		print "Server not reachable.  Saving best list to pickle to be safe."
		pickle.dump(route, open('backup.' + str(route_length_final(cities, route)) + '.p', 'wb'))
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
		self.client.sendPickle(C_REQ_UPDT, 'Hey bro, need an update!')
		sleep(5)
		while (self._stop == False):
			if (working == False):
				self.client.sendPickle(C_REQ_WORK, 'gimme work!')
			sleep(10)

#Initialize by asking for remote host info
clear()
HOST = raw_input("Server IP? (Defaults to mc.13-thirtyseven.com): ")
if (HOST == ''):
	HOST = 'mc.13-thirtyseven.com'
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
