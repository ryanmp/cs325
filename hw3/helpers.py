import math, random

def is_valid(cities,route):
	if len(cities) != len(route):
		return False
	test_route = route[:]
	test_route.sort()
	if [i for i in xrange(len(cities))] != test_route:
		return False
	return True


def distance(p1,p2):
	return math.hypot(p2[1]-p1[1],p2[0]-p1[0])

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