from helpers import *
import random

def algo_improve_swap2(cities,route,how_many_swaps):

	for i in xrange(len(cities)):

		new_route = route[0:]
		initial_length = route_length(cities,new_route)

		from1 = []
		to1 = []


		for j in xrange(how_many_swaps):

			from1.append(random.randint(0,len(cities)-1))
			to1.append(random.randint(0,len(cities)-1))

		for i in xrange(how_many_swaps):

			tmp1 = new_route[from1[i]]
			tmp2 = new_route[to1[i]]

			new_route[from1[i]] = tmp2
			new_route[to1[i]] = tmp1

		new_length = route_length(cities,new_route)

		if new_length < initial_length:
			print new_length
			route = new_route

	return route