import asyncore, asynchat, socket, threading
import signal, sys, pickle, os
from time import sleep

from helpers import *
from algo_fastdumb import *

#change these values only
PORT = 31337	# The port used by the server. Default 31337
DEBUG = False	# 3= show all packet data.
#change these values only

#Global Variables
connectionClassList = []
connectionSocketList = []
connectionHandlerList = []
shortest = sys.maxint		#Length of shortest path so far
cities = []			#List of cities
route = []			#Current best route
mode = 0			#Operating Mode
curGreedy = 0			#Current Starting City for greedy
curImprove = 1			#Current length for length improvements
curBackup = 0

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
S_IMP_SGT2 = 32 #S -> C #Send Improvement Work, swapping segments with wraparound
##Monitor / Control Packets##
M_GET_CURR = 40 #M -> S #Request current status
M_SET_MODE = 43 #M -> S #Request server mode change
M_LOAD_FIL = 44 #M -> S #Request server file load
M_SET_POSI = 45 #M -> S #Request server sets greedy & improve numbers
M_LOAD_PIC = 46 #M -> S #Request server loads route from file
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
	global curGreedy, curImprove, mode
	if DEBUG:
		print "Responding to work request.."
	if (mode == 0):
		self.sendPickle(KEEP_ALIVE, shortest)
	elif (mode == 1):
		self.sendPickle(S_WORK_GRE, curGreedy)
		curGreedy = curGreedy + 1
		if (curGreedy > len(cities)-1):
			curGreedy = 0
	elif (mode == 2):
		_pickle = pickle.dumps([curImprove, curImprove+18, route])
		dealMetaUpdate(self)
		self.sendPickle(S_IMP_SGMT, _pickle)
		curImprove = curImprove + 18
		if (curImprove > len(cities)/2):
			curImprove = 1
	elif (mode == 3):
		dealMetaUpdate(self)
		_pickle = pickle.dumps([curImprove, route])
		self.sendPickle(S_IMP_SCTY, _pickle)
		curImprove = curImprove + 1
		if (curImprove > len(cities)-1):
			curImprove = 0
	elif (mode == 4):
		_pickle = pickle.dumps([curImprove, route])
		dealMetaUpdate(self)
		self.sendPickle(S_IMP_SGT2, _pickle)
		curImprove = curImprove + 1
		if (curImprove > len(cities)/2):
			curImprove = 1
	else:
		print "something is horribly wrong"

#Handles requests for work from a client
def dealResult(self, payload):
	global shortest, route, cities, curBackup
	pickle.dump(route, open('backup.' + str(curBackup) + '.p', 'wb'))
	curBackup = curBackup + 1
	try:
		length = route_length_final(cities, payload)
		if DEBUG:
			print "we got a result!", length
		if (is_valid(cities, payload)):
			if (length < shortest):
				print self.addr, "Found a better Route!", shortest, ">", length
				shortest = length
				route = payload[0:]
		else:
			print self.addr, "Sent us an invalid route!"
			pickle.dump(route, open('backup.' + str(curBackup) + '.error.p', 'wb'))
			
	except Exception:
		print "got an invalid route!"

def dealLoadFile(self, payload):
	global cities, shortest, route, mode, curGreedy, curImprove
	print "Loading cities from file.", payload
	cities = parse_input("in/" + payload + ".txt")
	route = algo_fastdumb(cities)
	shortest = route_length_final(cities, route)
	mode = 0
	curGreedy = 0
	curImprove = 1
	for _handler in connectionHandlerList:
		try:
			print _handler.addr
			dealMetaUpdate(_handler)
		except Exception:
			connectionHandlerList.remove(_handler)
			pass

def dealRouteLoad(self, payload):
	global cities, shortest, route, mode, curGreedy, curImprove
	print "Loading route from file.", payload
	file = pickle.load(open("in/" + str(payload), 'rb'))
	route = file[0:]
	shortest = route_length_final(cities, route)
	mode = 0
	print "Loaded route", shortest
	for _handler in connectionHandlerList:
		try:
			print _handler.addr
			dealMetaUpdate(_handler)
		except Exception:
			connectionHandlerList.remove(_handler)
			pass

def dealModeChange(self, payload):
	global mode, curImprove
	mode = int(payload)
	if (mode == 2):
		curImprove = 1
	elif (mode == 3):
		curImprove = 0
	print "A connected monitor said we should switch to mode", int(payload)

#Handles a client asking for Monitor-info
def dealMonitorUpdate(self):
	global curGreedy, mode, curImprove
	addrList = []
	for _socketobject in connectionSocketList:
		try:
			addrList.append( _socketobject.getpeername() )
		except Exception:
			connectionSocketList.remove(_socketobject)
			pass
	_pickle = pickle.dumps([curGreedy, curImprove, mode, addrList])
	self.sendPickle(S_SEND_STA, _pickle)

def dealPositionChange(self, payload):
	global curGreedy, curImprove
	curGreedy, curImprove = pickle.loads(payload)

#The client asked for various meta-info, send it.
#Currently sends the length of shortest path so far,
#the list of cities, and the shortest path so far.
def dealMetaUpdate(self):
	global shortest, cities, route
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
		print "New client connecting:", addr
		connectionHandlerList.append(self)

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
			elif id == M_LOAD_FIL:
				dealLoadFile(self, payload)
				#Monitor says we should load a point set file.
			elif id == M_SET_MODE:
				dealModeChange(self, payload)
				#Monitor says we should go to another mode.
			elif id == M_SET_POSI:
				dealPositionChange(self, payload)
				#Monitor wants us to change positions.
			elif id == M_LOAD_PIC:
				dealRouteLoad(self, payload)
				#Monitor wants us to load route from file.
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
route = algo_fastdumb(cities)
shortest = route_length_final(cities, route)

#Run the event-driven server
print "Opening Socket..."
server = AsyncServer(PORT)
asyncore.loop(1)
