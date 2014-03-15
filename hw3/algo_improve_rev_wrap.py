from helpers import *


def algo_improve_rev_wrapper(cities,route,seg_length):

	#_length = len(cities)-seg_length
	_length = len(cities) # we can do the whole length now without issue
	for i in xrange(_length):

		start_idx = i
		end_idx = i+seg_length

		new_route = route[0:]
		initial_length = route_length(cities,new_route)

		# if we need to wrap
		if i+seg_length > len(cities):

			end = new_route[start_idx:]
			beginning = new_route[:end_idx%len(cities)]

			wrap = end + beginning

			wrap.reverse()

			new_beginning = wrap[len(end):]
			new_end = wrap[:len(end)]

			middle = new_route[end_idx%len(cities):start_idx]

			new_route = new_beginning + middle + new_end

			new_length = route_length(cities,new_route)
			if new_length < initial_length:
				#print route_length(cities,new_route), "wrapper"
				route = new_route

		# otherwise use the previous method
		else:
			tmp = new_route[start_idx:end_idx]
			tmp.reverse()
			new_route = route[:start_idx] + tmp + route[end_idx:]

			new_length = route_length(cities,new_route)
			if new_length < initial_length:
				#print route_length(cities,new_route), "norm"
				route = new_route



	return route


