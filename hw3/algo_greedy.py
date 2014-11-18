import sys, math

'''
from a starting city, it continually adds the next closest city to the route
'''

def algo_greedy(cities):
	route = [cities[0]]
	unvisited = cities[1:]
	while unvisited:
		closest_dist = sys.maxint
		closest_idx = 0
		for i in unvisited:
			#distance = math.hypot(i[0] - route[-1][0], i[1] - route[-1][1])
			distance = add(math.pow(i[0] - route[-1][0], 2), math.pow((i[1] - route[-1][1]), 2))
			if (distance < closest_dist):
				closest_dist = distance
				closest_idx = i
		route.append(closest_idx)
		unvisited.remove(closest_idx)

	route2 = []
	for i in route:
		route2.append(cities.index(i))

	return route2

#Same as algo_greedy, but accepts a parameter to choose what city to start at.
#This is for use when you want to calculate greedy from multiple starting positions
#But not all (algo_greedy_all)  Used solely for the server to distribute work to clients.
def algo_greedy_start(cities, _start):
	_cities = cities[0:]		#create local copy (workaround)
	_route = [_cities[_start]]	#initialize to starting city
	_cities.pop(_start)		#pop off the starting city
	unvisited = _cities[0:]		#Again, make sure we have a local copy
	while unvisited:
		closest_dist = sys.maxint
		closest_idx = 0
		for i in unvisited:
			distance = math.hypot(i[0] - _route[-1][0], i[1] - _route[-1][1])
			if distance < closest_dist:
				closest_dist = distance
				closest_idx = i
		_route.append(closest_idx)
		unvisited.remove(closest_idx)

	route2 = []
	for i in _route:
		route2.append(cities.index(i))

	return route2
