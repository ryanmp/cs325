from helpers import *
import random


def algo_improve_combo(cities,route,seg_length):

	#_length = len(cities)-seg_length
	_length = len(cities) # we can do the whole length now without issue
	for i in xrange(_length):


		##### stage1

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

		# otherwise use the previous method
		else:
			tmp = new_route[start_idx:end_idx]
			tmp.reverse()
			new_route = route[:start_idx] + tmp + route[end_idx:]

		###### stage 2
		# transpose


		idx = random.randint(0,len(cities))
		start = new_route[:idx]
		middle = new_route[idx:idx+seg_length]
		end = new_route[idx+seg_length:]
		new_route = start + end + middle

		new_length = route_length(cities,new_route)
		if new_length < initial_length:
			route = new_route

	return route


