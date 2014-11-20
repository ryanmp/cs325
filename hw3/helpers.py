import math, random, os, platform

#helper method to Clear the screen, on all OS's
def clear():
	if (platform.system() == "Windows"):
		os.system('cls')
	else:
		os.system('clear')

#Checks if a given route is valid for a given set of cities.
#This is our own implementation, not the teacher's checker.
def is_valid(cities,route):
	if len(cities) != len(route):
		return False
	test_route = route[:]
	test_route.sort()
	if [i for i in xrange(len(cities))] != test_route:
		return False
	return True

#Reads in a list of cities to calculate a route on.
def parse_input(file_name):
	f = open(file_name)
	lines_raw = f.readlines()
	ret = []
	for i in range(0,len(lines_raw)):
		parsing_line = []
		parsing_line = lines_raw[i].split()
		parsing_line = map(int, parsing_line)
		to_tuple = (parsing_line[1],parsing_line[2])
		ret.append(to_tuple)
	return ret

#Calculates the distance between 2 points.
def distance(p1,p2):
	return math.hypot(p2[1]-p1[1],p2[0]-p1[0])

#Runs the teacher's route validity checker.
def run_verifier(cities_txt,route_txt):
	path = os.getcwd() + "/"
	os.system("python tsp-verifier.py "+path+cities_txt+" "+path+route_txt)

#Wites a route to the format that we need to turn in.
def format_output(cities, route, file_name):
	#create a file
	f = open(file_name, "wb")

	#first line is the route length as an int
	#i'm using a new route_length function, because tsp-verifier needs
	#a lot of rounding
	route_length_str = str(int(route_length_final(cities,route)))+"\n"
	f.write(route_length_str)

	#write each city in route as new line
	for i in route:
		f.write(str(i)+"\n")
	f.close()

def route_length(cities,route):
	distance = 0
	_length = len(route)-1
	for i in xrange(_length):
		idx1 = route[i]
		idx2 = route[i+1]
		distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])
	
	#connect back to start
	idx1 = route[-1]
	idx2 = route[0]

	distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])

	return distance

def route_length_final(cities,route):
	distance = 0
	_length = len(route)-1
	for i in xrange(_length):
		idx1 = route[i]
		idx2 = route[i+1]

		dy = cities[idx2][0] - cities[idx1][0] # now we are calculating it the same way as tsp-verifier
		dx = cities[idx2][1] - cities[idx1][1]
		distance += int(round(math.sqrt(dx*dx + dy*dy)))
		#distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])
	
	#connect back to start
	idx1 = route[-1]
	idx2 = route[0]
	dy = cities[idx2][0] - cities[idx1][0]
	dx = cities[idx2][1] - cities[idx1][1]
	distance += int(round(math.sqrt(dx*dx + dy*dy)))
	#distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])

	return distance

#Used for finding the length of just a specific segment of a route.
def segment_length(cities,route,_start,_end):
	distance = 0
	_length = len(route)-1
	for i in xrange(_start-1,_end):
		idx1 = route[i]
		try:
			idx2 = route[i+1]
		except Exception:	#Kinda a hackjob, but hey, it works.
			return sys.maxint
		distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])
	return distance

def generate_test_set(_list_length,_max_int):
	global set
	random.seed("0")    #Seeds the RNG.  This causes us to use the same test set every run.
	set = []
	for i in xrange(_list_length):
		set.append((random.randrange(1,_max_int),random.randrange(1,_max_int)))
	return set

def return_set(max):
	global set
	#not done
	return set[:max]
