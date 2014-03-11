import itertools
from tree import *
from helpers import *
import time

#minimum spanning tree

#input: list of cities
#output: tree representation of edges for MST -> traversal -> route


#@profile
def algo_mst(cities):

	all_edges = set() #(cityA,cityB,distance)

	# setting up our city-set as a set of edges
	for idx1 in xrange(len(cities)):

		for idx2 in range(idx1+1,len(cities)):
			new = (idx1,idx2,distance(cities[idx1],cities[idx2]))
			all_edges.add(new)

	# vertices
	v_not_in_tree = set([i for i in xrange(len(cities))])

	# just pick a starting node...
	v_in_tree = set([0])
	tree=Node('0')

	while (len(v_not_in_tree) > 1): 

		# set of edges connected to the nodes of our tree (but not already in tree)
		possible_new_edges = []
		for v in v_in_tree:
			filter_result = filter(
				lambda x: ((x[1] == v or x[0] == v)
					and not( x[0] in v_in_tree and x[1] in v_in_tree)) , 
				all_edges) 
			possible_new_edges.append( filter_result )
		possible_new_edges = list(itertools.chain(*possible_new_edges)) #flatten 2d list to 1d

		# which edge has the minimum weight?
		next_edge = min(possible_new_edges, key = lambda t: t[2])

		# is arg0 or arg1 the new node?
		# let's add this new edge to the tree while we are at it
		if (next_edge[0] in v_in_tree):
			v = next_edge[1]
			tree.add_child2(str(next_edge[0]),str(next_edge[1]))
		else: 
			v = next_edge[0]
			tree.add_child2(str(next_edge[1]),str(next_edge[0]))

		all_edges.remove(next_edge)
		v_in_tree.add(v)
		v_not_in_tree.remove(v)

	# pre order trav that shit and we are done
	return map(int,pre_order_trav(tree))





