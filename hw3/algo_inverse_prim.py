import sys, math, numpy
from helpers import *


'''

creates a list of all distances
    while listlen > cities*2:
        if removing max doesn't break loop (every node still has at least 2 edges)
            remove max distance from distances
        else, add max into route
        
'''

def algo_inverse_prim(cities):
   
    # what do we need to know about our cities when described as a graph?
    distances = []
    edges = []
    edge_per_node_count = [0 for i in xrange(len(cities))]

    # setting up our graph (distances, edges, node-edge-count)
    for idx1 in xrange(len(cities)):
        for idx2 in range(idx1,len(cities)):
            if (idx1 != idx2):
                distances.append(distance(cities[idx1],cities[idx2]))
                edges.append((idx1,idx2))
                edge_per_node_count[idx1] += 1
                edge_per_node_count[idx2] += 1

    route_as_edges = edges

    print "all distances:",distances
    print "------"

    for i in distances:

        biggest = numpy.argmax(distances)
        i = route_as_edges[biggest][0]
        j = route_as_edges[biggest][1]
        if edge_per_node_count[i] > 2 and edge_per_node_count[j] > 2 :
            
            print "." 
            distances.pop(biggest)
            route_as_edges.pop(biggest)
            edge_per_node_count[i] -= 1
            edge_per_node_count[j] -= 1
        else:
            distances.pop(biggest)

        #if len(route_as_edges) <= len(cities):
        #    return distances, edges

    #convert list of edges back to a route

    print edges

    route = []

    route.append(edges[0][0])
    next = edges.pop(0)

    while (len(route) < len(cities)):
        this = filter(lambda x: x[0] == next[1], edges)
        if (not len(this) > 0): this = filter(lambda x: x[1] == next[1], edges)
        route.append(this[0][0])
        next = this[0]
        edges.remove(this[0])
        print edges, route

    print edges,route





