import itertools, sys, math

from helpers import *

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
