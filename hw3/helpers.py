import math, random

def distance(p1,p2):
	return math.hypot(p2[1]-p1[1],p2[0]-p1[0])

def route_length(cities,route):
	distance = 0
	for i in xrange(len(route)-1):
		idx1 = route[i]
		idx2 = route[i+1]
		distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])
	
	#connect back to start
	idx1 = route[-1]
	idx2 = route[0]
	distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])

	return distance

def path_length(cities,route):
	distance = 0
	for i in xrange(len(route)-1):
		idx1 = route[i]
		idx2 = route[i+1]
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