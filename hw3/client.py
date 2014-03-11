import signal

#change these values only
PORT = 31337		# The port used by the server. Default 31337
DEBUG = True
#change these values only

#Global Variables
derp = []

#Packet Constants#
KEEP_ALIVE = 0  #C -> S #Keep-alive
C_REQ_WORK = 1  #C -> S #Request for work
C_SEND_RES = 2  #C -> S #rend result
C_REQ_UPD  = 3  #C -> S #request meta-info update
##Server Packets##
S_SEND_UPD = 10 #S -> C #send meta-info update
S_WORK_GRE = 11 #S -> C #send greedy algorithm work
S_WORK_MST = 12 #S -> C #send MST algorithm work
##Improvement Packets##
S_IMP_SGMT = 15 #S -> C #Send improvement work, swapping segments
S_IMP_SCTY = 16 #S -> C #send improvement work, swapping cities

def signal_handler(signum, frame):
	server.sendKill();
	if signum == 2:
		signum = 'Control-c'
	print 'SHUTDOWN!  Reason:', signum
	#sleep(1)
	#exit()

	def sendKill(self):
		print "Sorry, I've disabled killing the client using control-c, as It could conceivably cause some data to be lost, if it is done at a very bad time for the server."

#set up signal handler(s)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)