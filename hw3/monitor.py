import asyncore, asynchat, socket, threading
import signal, pickle, sys, os, curses
from time import sleep
from sys import stdout, exit

from helpers import *
from algo_greedy import *
from algo_mst import *
from algo_improve_rev import *
from algo_improve_swap import *

#change these values only
DEBUG = True	# 3= show all packet data.
#change these values only

#Global Variables
shortest = sys.maxint
cities = []
route = []
mode = "unknown"
curGreedy = "unknown"
curImprove = "unknown"
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
M_LOAD_FIL = 44 #M -> S #Request server file load
M_SET_POSI = 45 #M -> S #Request server stets greedy & improve numbers
M_LOAD_PIC = 46 #M -> S #Request server loads route from file
##Server (monitor) Reply Packets##
S_SEND_STA = 50 #S -> M #Respond with current status

def signal_handler(signum, frame):
	print "Closing socket..."
	sleep(2)
	client.t.stop()
	sleep(2)
	exit()

def dealMetaInfoUpdate(self, payload):
	global shortest, cities, route
	shortest, cities, route = pickle.loads(payload)

def dealStatusUpdate(self, payload):
	global mode, clients, curGreedy, curImprove
	curGreedy, curImprove, mode, clients = pickle.loads(payload)

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
		pickle.dump(route, open('monitor_backup.' + str(route_length_final(cities, route)) + '.p', 'wb'))
		curses.endwin()
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
		curses.endwin()

	#What the thread actually does
	def run(self):
		while (self._stop == False):
			print "starting initial queries..."
			self.client.sendPickle(C_REQ_UPDT, 'M update')
			sleep(1)
			self.client.sendPickle(M_GET_CURR, 'M Status')
			sleep(5)
			
			def get_param(prompt_string):
				screen.clear()
				screen.border(0)
				screen.addstr(2, 2, prompt_string)
				screen.refresh()
				screen.timeout(999999999)
				input = screen.getstr(10, 10, 60)
				return input
			x = 0
			while x != ord('5'):
				screen = curses.initscr()
				screen.clear()
				screen.border(0)
				screen.addstr(2, 8, "Welcome to Joshua Villwock's")
				screen.addstr(3, 9, "CS381 Server Control Centre")
				screen.addstr(14, 2, "Please enter a number...")
				screen.addstr(16, 4, "1 - Switch server mode")
				screen.addstr(17, 4, "2 - Load a List in ./in/*.txt")
				screen.addstr(18, 4, "3 - Load a Route in ./in/*.p")
				screen.addstr(19, 4, "4 - Change Progress")
				screen.addstr(20, 4, "5 - Exit")
				screen.addstr(22, 4, "7 - Dump Route to ./out/" + str(shortest) + ".txt")

				screen.addstr(5, 6, "#cities:  ")
				screen.addstr(6, 6, "#c's in r:")
				screen.addstr(7, 6, "shortest: ")
				screen.addstr(8, 6, "greedy:   ")
				screen.addstr(9, 6, "Improve:  ")
				screen.addstr(10, 6, "Clients:  ")
				screen.addstr(11, 6, "Mode:     ")
				screen.addstr(12, 6, "Valid?:   ")
				global mode
				screen.addstr(5, 17, str(len(cities)))
				screen.addstr(6, 17, str(len(route)))
				screen.addstr(7, 17, str(shortest))
				screen.addstr(8, 17, str(curGreedy))
				screen.addstr(9, 17, str(curImprove))
				screen.addstr(10, 17, str(len(clients)))
				screen.addstr(11, 17, str(mode))
				screen.addstr(12, 17, str(is_valid(cities,route)))

				screen.refresh()
				self.client.sendPickle(C_REQ_UPDT, 'M update')
				self.client.sendPickle(M_GET_CURR, 'M Status')
				screen.timeout(5000)
				x = screen.getch()
				if x == ord('1'):
					mode = get_param("0=idle, 1=greedy, 2=route improve, 3=city improve, 4=route w/ wrap")
					self.client.sendPickle(M_SET_MODE, int(mode))
				elif x == ord('2'):
					file = get_param("File Name?")
					self.client.sendPickle(M_LOAD_FIL, file)
				elif x == ord('3'):
					file = get_param("File name?")
					self.client.sendPickle(M_LOAD_PIC, file)
				elif x == ord('4'):
					greedy_pos = get_param("Greedy Position?")
					imp_pos = get_param("Improvement Position?")
					_pickle = pickle.dumps([int(greedy_pos), int(imp_pos)])
					self.client.sendPickle(M_SET_POSI, _pickle)
				elif x == ord('7'):
					curses.endwin()
					format_output(cities, route, "out/" + str(shortest) + ".txt")
					run_verifier("in/example-input-3.txt","out/" + str(shortest) + ".txt")
			curses.endwin()
			print "Exiting Monitor..."
			self._stop = True
			self.client.close()
			sleep(1)
			self.client.t.stop()
			sleep(1)
			exit()

#Initialize by asking for remote host info
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
curses.endwin()
