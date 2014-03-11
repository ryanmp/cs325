import asyncore
import socket
import json
import signal
import threading
from time import sleep
from sys import stdout, exit

#change these values only
PORT = 31337		# The port used by the server. Default 31337
DEBUG = True
#change these values only

#Global Variables
connectionClassList = []
connectionSocketList = []

#constants#
KEEP_ALIVE = 0
C_REQ_WORK = 1
C_SEND_RES = 2
C_UPDATE_M = 3
S_UPDATE_M = 10
S_WORK_AG = 11

#deal with signals
def signal_handler(signum, frame):
	server.sendKill();
	if signum == 2:
		signum = 'Control-c'
	print 'SHUTDOWN!  Reason:', signum
	sleep(1)
	exit()

#Returns a json-formatted string based on the packet ID and packet payload
def createJson(self, id, payload):
	_json = json.dumps( {"id":id, "payload":payload} )
	return _json

#If client sends us a packet ID 0 (keep-alive)
#Then just pong one back to the client
def dealKeepAlive(self, payload):
	print 'replying to keep-alive from:', self.addr
	self.send( createJson(self, 0, payload) )

#Client asked for a range of numbers they should check
#Send them however many they asked for
def dealRangeReq(self, quantity):
	global currNum
	if DEBUG:
		print 'replying to request for', quantity, 'numbers from:', self.addr
	self.send( createJson(self, 2, currNum) )
	currNum += quantity

#The Client sent us a number that they say is a perfect number!
#Amazing!  Make a note of this!
def dealNumberFound(self, address, numberFound):
	print 'client', address[0],':',address[1], 'claims that', numberFound, 'is a perfect number!'
	perfectNumbersFound.append(numberFound)
	
def dealReportFound(self):
	if DEBUG:
		print 'A Reporter has asked for the numbers we have found.  Sending.'
	self.send( createJson(self, 5, perfectNumbersFound) )

def dealReportClients(self):
	if DEBUG:
		print 'A Reporter has asked for our connection List.  Sending.'
	addrList = []
	for _socketobject in connectionSocketList:
		try:
			addrList.append( _socketobject.getpeername() )
		except Exception:
			print 'derp'
			pass
	self.send( createJson(self, 6, addrList) )

def dealReportNumber(self):
	if DEBUG:
		print 'A Reporter has asked for how far we are currently.  Sending.'
	self.send( createJson(self, 7, currNum) )

#Class For handling the event-driven server
class PacketHandler(asyncore.dispatcher_with_send):
	def setAddr(self, address):
		self.addr = address

	#probably not needed any more
	def setSock(self, sock2):
		self.sock = sock2

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
			elif data['id'] == 1:
				quantity = data['payload']
				dealRangeReq(self, quantity)
			elif data['id'] == 3:
				numberFound = data['payload']
				dealNumberFound(self, self.addr, numberFound)
			elif data['id'] == 5:
				dealReportFound(self)
			elif data['id'] == 6:
				dealReportClients(self)
			elif data['id'] == 7:
				dealReportNumber(self)
			elif data['id'] == 9:
				sleep(5)
				signal_handler('Got Kill Packet From Client', 'derp')
			else:
				print 'something went wrong.'

#Class that sets up the event-driven server
#and passes data it receives to the PacketHandler() class
class AsyncServer(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(("", port))
		self.listen(5)
		print 'server is now listening for connections.'

	#We have been told to shutdown!
	#Make sure we send the shutdown packet first!
	def sendKill(self):
		for _socketobject in connectionSocketList:
			try:
				_socketobject.send( createJson(self, 9, 'Server says SHUTDOWN!') )
				print str( _socketobject.getpeername()[0] ) + ':' + str( _socketobject.getpeername()[1] ) + ' was sent the shutdown signal!'
			except Exception:
				pass

	#We got a client connection!
	def handle_accept(self):
		pair = self.accept()
		if pair is None:
			print 'something is messed up'
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
		#for _socketobject in connectionSocketList:
		#	if _socketobject.getpeername()[0] == self.sock.getpeername()[0]
		#		print 'derp'
		#		connectionSocketList.remove(self.sock)
		#	else
		#		print 'herp'

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)

#Run the event-driven server
server = AsyncServer('', PORT)
asyncore.loop(1)