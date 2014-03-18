from helpers import *

def algo_improve_swap(cities, route, i):

	for j in xrange(len(cities)):

		new_route = route[0:]
		initial_length = route_length(cities,new_route)

		tmp1 = new_route[i]
		tmp2 = new_route[j]
		new_route[i] = tmp2
		new_route[j] = tmp1

		new_length = route_length(cities,new_route)

		if new_length < initial_length:
			print j, new_length
			route = new_route

	return route