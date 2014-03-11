import itertools
from tree import *
from helpers import *

#minimum spanning tree

#input: list of cities
#output: tree representation of edges for MST -> traversal -> route

def algo_mst(cities):

	all_edges = [] #(cityA,cityB,distance)

	# setting up our city-set as a set of edges
	for idx1 in xrange(len(cities)):
		for idx2 in range(idx1+1,len(cities)):
			all_edges.append((idx1,idx2,distance(cities[idx1],cities[idx2])))

	# vertices
	v_not_in_tree = [i for i in xrange(len(cities))]

	# just pick a starting node...
	v_in_tree = [v_not_in_tree.pop()]

	tree=Node(str(v_in_tree[0]))

	while (len(v_not_in_tree) > 0): 
		# set of edges connected to the nodes of our tree
		possible_new_edges = []
		for v in v_in_tree:
			possible_new_edges.append( filter(lambda x: x[1] == v or x[0] == v , all_edges) )
		possible_new_edges = list(itertools.chain(*possible_new_edges)) #flatten 2d list to 1d

		# removing any edges that are already in our tree
		to_remove = []
		for i in possible_new_edges:
			if i[0] in v_in_tree and i[1] in v_in_tree:
				to_remove.append(i)

		possible_new_edges = list(set(possible_new_edges) - set(to_remove))

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
		v_in_tree.append(v)
		v_not_in_tree.remove(v)

	return map(int,pre_order_trav(tree))

