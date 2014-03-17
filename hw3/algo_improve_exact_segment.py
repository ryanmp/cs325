import itertools
from helpers import *

def algo_improve_exact_segment(cities,route,start_idx, end_idx):

	return_route = route[:]

	part_of_route = route[start_idx:end_idx]
	all_routes =  list(itertools.permutations(part_of_route))

	current_length = route_length(cities,route)

	for i in all_routes:
		new_route = route[:start_idx] + list(i) + route[end_idx:]
		new_length = route_length(cities,new_route)
		if new_length < current_length:
			return_route = new_route
			current_length = new_length

	return return_route

