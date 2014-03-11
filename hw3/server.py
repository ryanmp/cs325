import asyncore, socket, signal, threading, sys, pickle
from time import sleep

from helpers import *

#change these values only
PORT = 31337		# The port used by the server. Default 31337
DEBUG = True		# Output all kinds of random junk you probly really don't want to see?
#change these values only

#Global Variables
connectionClassList = []
connectionSocketList = []
shortest = sys.maxint
cities = []
route = []

#Packet Constants#
KEEP_ALIVE = 0  #C -> S #Keep-alive
C_REQ_WORK = 1  #C -> S #Request for work
C_SEND_RES = 2  #C -> S #Send result
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

#deal with signals
def signal_handler(signum, frame):
	server.sendKill();
	if signum == 2:
		signum = 'Control-c'
	print 'SHUTDOWN!  Reason:', signum
	sleep(1)
	exit()

#Returns a pickle-formatted string based on the packet ID and packet payload
def createPickle(self, id, payload):
	_pickle = pickle.dumps([id, payload])
	return _pickle

def metaPack(self, shortest, cities, route):
	_pickle = pickle.dumps([shortest, cities, route])
	return _pickle

#If client sends us a packet ID 0 (keep-alive)
#Then just pong one back to the client
#I think this is obsolete now, keeping to be safe.
def dealKeepAlive(self, payload):
	print 'replying to keep-alive from:', self.addr
	self.send( createPickle(self, KEEP_ALIVE, payload + " reply") )

#Client asked for a range of numbers they should check
#Send them however many they asked for
#def dealRangeReq(self, quantity):
#	global currNum
#	if DEBUG:
#		print 'replying to request for', quantity, 'numbers from:', self.addr
#	self.send( createPickle(self, 2, currNum) )
#	currNum += quantity

#The Client sent us a number that they say is a perfect number!
#Amazing!  Make a note of this!
#def dealNumberFound(self, address, numberFound):
#	print 'client', address[0],':',address[1], 'claims that', numberFound, 'is a perfect number!'
#	perfectNumbersFound.append(numberFound)
	
#def dealReportFound(self):
#	if DEBUG:
#		print 'A Reporter has asked for the numbers we have found.  Sending.'
#	self.send( createPickle(self, 5, perfectNumbersFound) )

#def dealReportClients(self):
#	if DEBUG:
#		print 'A Reporter has asked for our connection List.  Sending.'
#	addrList = []
#	for _socketobject in connectionSocketList:
#		try:
#			addrList.append( _socketobject.getpeername() )
#		except Exception:
#			print 'derp'
#			pass
#	self.send( createPickle(self, 6, addrList) )

def dealRequest(self, payload):
	if DEBUG:
		print "Request for work being handled!"
	self.send(createPickle(self, S_WORK_GRE, 7))
	#7 is a placeholder.  PLEASE FIX

def dealMetaUpdate(self):
	if DEBUG:
		print "Request for meta-info update being handled."
	_pickle = metaPack(self, shortest, cities, route)
	self.sendall(createPickle(self, S_SEND_UPD, _pickle))
	
#Class For handling the event-driven server
class PacketHandler(asyncore.dispatcher_with_send):
	def setAddr(self, address):
		self.addr = address

	#probably not needed any more
	def setSock(self, sock2):
		self.sock = sock2

	def handle_read(self):
		data = self.recv(8192)
		#lets load up that pickle!  (DOES NOT DEAL WITH INVALID PICKLE!)
		id, payload = pickle.loads(data)
		#assuming we actually received SOMETHING.....
		if data:
			if DEBUG:
				print data
			if id == KEEP_ALIVE:
				dealKeepAlive(self, payload)
			elif id == C_REQ_WORK:
				dealRequest(self, payload)
			elif id == C_SEND_RES:
				print "Hey, we got a result.  Deal with it."
				#dealResult(self, self.addr, payload)
			elif id == C_REQ_UPDT:
				print "this is just here to make python happy."
				dealMetaUpdate(self)
			elif id == 9:
				sleep(5)
				signal_handler('Got Kill Packet From Client', 'derp')
			else:
				print 'something went wrong.', id, payload

#Class that sets up the event-driven server
#and passes data it receives to the PacketHandler() class
class AsyncServer(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(("", port))
		self.listen(5)
		print 'Server is now listening for connections.'

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
			handler = PacketHandler(sock)
			handler.setAddr(addr)
			handler.setSock(sock)
			connectionClassList.append(self)
			connectionSocketList.append(sock)

	def handle_close():
		print self.addr, 'has disconnecteed!'
		self.close()

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#Set up
print "Setting up server..."
generate_test_set(15000,4000)
cities = return_set(15000)

#Run the event-driven server
server = AsyncServer('', PORT)
asyncore.loop(1)