import asyncore, asynchat, socket, threading
import signal, sys, pickle, os
from time import sleep

from helpers import *

#change these values only
PORT = 31337	# The port used by the server. Default 31337
DEBUG = True	# 3= show all packet data.
#change these values only

#Global Variables
connectionClassList = []
connectionSocketList = []
shortest = sys.maxint	#Length of shortest path so far
cities = []				#List of cities
route = []				#Current best route
mode = 1				#Operating Mode
curGreedy = 0			#Current Starting City for greedy
curImprove = 1			#Current length for length improvements

#Packet Constants#
KEEP_ALIVE = 0  #C -> S #Keep-alive
C_REQ_WORK = 1  #C -> S #Request for work
C_SEND_RES = 2  #C -> S #Send result
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

#deal with signals
def signal_handler(signum, frame):
	server.sendKill();
	if signum == 2:
		signum = 'Control-c'
	print 'SHUTDOWN!  Reason:', signum
	sleep(1)
	exit()

#helper method to Clear the screen
def clear():
	os.system('cls')
	os.system('clear')

#Returns a pickle-formatted string based on the packet ID and packet payload
def createPickle(self, id, payload):
	_pickle = pickle.dumps([id, payload])
	return _pickle

#Packs meta-info up to send to the client
def metaPack(self, shortest, cities, route):
	_pickle = pickle.dumps([shortest, cities, route])
	return _pickle

#If client sends us a packet ID 0 (keep-alive)
#Then just pong one back to the client
#I think this is obsolete now, keeping to be safe.
def dealKeepAlive(self, payload):
	print 'Responding to keep-alive from:', self.addr
	self.sendPickle(KEEP_ALIVE, payload + " reply")

#Actually handles requests for work.
#For now, this just sends a static packet, to test.
def dealRequest(self, payload):
	global curGreedy, curImprove
	if DEBUG:
		print "Responding to work request.."
	if (mode == 1):
		self.sendPickle(S_WORK_GRE, curGreedy)
		curGreedy = curGreedy + 1
	elif (mode == 2):
		_pickle = pickle.dumps([curImprove, curImprove+50, route])
		dealMetaUpdate(self)
		sleep(3)
		self.sendPickle(S_IMP_SGMT, _pickle)
		curImprove = curImprove + 50
		if (curImprove > len(cities)/2):
			curImprove = 1
	elif (mode == 3):
		print "not implemented yet! (city swap)"
	else:
		print "something is horribly wrong"

#Handles requests for work from a client
def dealResult(self, payload):
	global shortest, route
	length = route_length_final(cities, payload)
	if DEBUG:
		print "we got a result!", length
	if (length < shortest):
		print self.addr, "Found a better Route!", shortest, ">", length
		shortest = length
		route = payload[0:]

def dealModeChange(self, payload):
	global mode
	mode = payload
	print "A connected monitor said we should switch to mode", payload

#Handles a client asking for Monitor-info
def dealMonitorUpdate(self):
	global curGreedy, mode, curImprove
	addrList = []
	for _socketobject in connectionSocketList:
		try:
			addrList.append( _socketobject.getpeername() )
		except Exception:
			pass
	_pickle = pickle.dumps([curGreedy, curImprove, mode, addrList])
	self.sendPickle(S_SEND_STA, _pickle)

#The client asked for various meta-info, send it.
#Currently sends the length of shortest path so far,
#the list of cities, and the shortest path so far.
def dealMetaUpdate(self):
	if (DEBUG == 3):
		print "Responding to meta-info update request."
	_pickle = metaPack(self, shortest, cities, route)
	self.sendPickle(S_SEND_UPD, _pickle)

#Class For handling the event-driven server
class PacketHandler(asynchat.async_chat):
	def __init__(self, _sock, addr):
		asynchat.async_chat.__init__(self, _sock)
		self.set_terminator("\r\n\r\n")
		self.request = None
		self.data = ""
		self.sock = _sock
		self.addr = addr
		if DEBUG:
			print "New client connecting:", addr

	def collect_incoming_data(self, data):
		self.data = self.data + data

	def found_terminator(self):
		data = self.data
		self.data = ""
		#lets load up that pickle!  (DOES NOT DEAL WITH INVALID PICKLE!)
		id, payload = pickle.loads(data)
		#assuming we actually received SOMETHING.....
		if data:
			if (DEBUG == 3):
				print id, payload
			if id == KEEP_ALIVE:
				dealKeepAlive(self, payload)
				#Client Sent keep-alive.  Reply to it.
			elif id == C_REQ_WORK:
				dealRequest(self, payload)
				#Client Requested work.  Call work handling Function
			elif id == C_SEND_RES:
				dealResult(self, payload)
				#Hey, we got a result.  Deal with it.
			elif id == C_REQ_UPDT:
				dealMetaUpdate(self)
				#Client requested Meta-info update.  Call function to send it.
			elif id == M_GET_CURR:
				dealMonitorUpdate(self)
				#Monitor is asking for info
			elif id == M_SET_MODE:
				dealModeChange(self, payload)
				#Monitor says we should go to another mode.
			else:
				print 'something went wrong.', id, payload

	def sendPickle(self, id, payload):
		self.push(pickle.dumps([id, payload]) + "\r\n\r\n")

#Class that sets up the event-driven server
#and passes data it receives to the PacketHandler() class
class AsyncServer(asyncore.dispatcher):
	def __init__(self, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(("", port))
		self.listen(5)
		print 'Server is now listening for connections.'

	def handle_request(self, channel, method, path, header):
		print "blah"

	#We have been told to shutdown!
	#Make sure we send the shutdown packet first!
	def sendKill(self):
		for _socketobject in connectionSocketList:
			try:
				_socketobject.send( createPickle(self, S_SERV_KIL, 'Server says SHUTDOWN!') )
				print str( _socketobject.getpeername()[0] ) + ':' + str( _socketobject.getpeername()[1] ) + ' was sent the shutdown signal!'
			except Exception:
				pass

	#We got a client connection!
	def handle_accept(self):
		pair = self.accept()
		if pair is None:
			print 'something is messed up', pair
			pass
		else:
			sock, addr = pair
			handler = PacketHandler(sock, addr)
			connectionClassList.append(self)
			connectionSocketList.append(sock)

	def handle_close(self):
		print self.addr, 'has disconnecteed!'
		self.close()

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#Set up
clear()
print "Setting up server..."
generate_test_set(15000,4000)
cities = return_set(15000)

#Run the event-driven server
print "Opening Socket..."
server = AsyncServer(PORT)
asyncore.loop(1)