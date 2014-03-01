import itertools, sys, math

'''

calculates the length of every possible route (list gen via itertools permutations)
returns the route with the shortest length

'''

def algo_exact(cities):
	a_route = [i for i in xrange(len(cities))]
	all_routes =  list(itertools.permutations(a_route))
	shortest_path_len = sys.maxint
	shortest_path_idx = 0
	for i in xrange(len(all_routes)):
		this_len = route_length(cities,all_routes[i])
		if this_len < shortest_path_len:
			shortest_path_len = this_len
			shortest_path_idx = i

	return all_routes[shortest_path_idx]

def route_length(cities,route):
	distance = 0
	for i in xrange(len(route)-1):
		idx1 = route[i]
		idx2 = route[i+1]
		distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])
	return distance