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

def route_length_hash(cities,route,dict_distances):
	distance = 0
	for i in xrange(len(route)-1):
		idx1 = route[i]
		idx2 = route[i+1]

	 	# ouch look at the format of that key
        k1 = '('+str(cities[idx2][0])+', '+str(cities[idx2][1])+')('+str(cities[idx1][0])+', '+str(cities[idx1][1])+')'
        k2 = '('+str(cities[idx1][0])+', '+str(cities[idx1][1])+')('+str(cities[idx2][0])+', '+str(cities[idx2][1])+')'
        # two possible orderings: city1, city2 or city2, city1
        try:
            distance = dict_distances[k1]
        except:
            distance = dict_distances[k2]

	#connect back to start
	idx1 = route[-1]
	idx2 = route[0]

	distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])

	return distance

def route_length_final(cities,route):
	distance = 0
	for i in xrange(len(route)-1):
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