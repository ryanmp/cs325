from helpers import *


def algo_improve_transpose(cities,route):

	#print "input", route

	for i in xrange(3):

		print i

		for j in xrange(20):

			if (i != j):
				new_route = route[0:]

				initial_length = route_length(cities,new_route)
				middle = new_route.pop(i)

				new_route.insert(j,middle)

				new_length = route_length(cities,new_route)

				if new_length < initial_length:
					print new_length
					route = new_route

	return route

