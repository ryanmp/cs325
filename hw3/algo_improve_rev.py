from helpers import *

def algo_improve_rev(cities,route,seg_length):

	_length = len(cities)-seg_length
	for i in xrange(_length):

		start_idx = i
		end_idx = i+seg_length

		new_route = route[0:]
		initial_length = segment_length(cities,new_route,start_idx,end_idx)

		tmp = new_route[start_idx:end_idx]
		tmp.reverse()
		new_route[start_idx:end_idx] = tmp

		new_length = segment_length(cities,new_route,start_idx,end_idx)

		if new_length < initial_length:
			route = new_route

	return route