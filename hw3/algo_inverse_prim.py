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
    print "all edges:",route_as_edges
    print "------"


    idx = 0
    while len(distances) - idx >= len(cities):
        biggest = numpy.argmax(distances)

        print "biggest", biggest

        i = edges[biggest][0]
        j = edges[biggest][1]

        print "biggest - ", distances[biggest],i,j

        if (edge_per_node_count[i] > 2 and edge_per_node_count[j] > 2):
            distances[biggest] = -1
            idx += 1
            route_as_edges[biggest] = -1
            edge_per_node_count[i] -= 1
            edge_per_node_count[j] -= 1
            print ":::",route_as_edges, edge_per_node_count
        else:
            print "can't do it!"
            print len(distances)
            distances[biggest] = -1
            print ":::",route_as_edges, edge_per_node_count



    #convert list of edges back to a route


    edges2 = []
    for i in edges:
        if (i != -1):
            edges2.append(i)
    edges = edges2

    print "finalish", edges

    route = []
    route.append(edges[0])
    next = edges.pop(0)

    print "next",next

    while (len(route) < len(cities)):
        print "lengths:",len(route),len(cities)
        this = filter(lambda x: x[0] == next[1], edges)
        print this
        if (not len(this) > 0): this = filter(lambda x: x[1] == next[1], edges)
        print this
        if (not len(this) > 0): this = filter(lambda x: x[0] == next[0], edges)
        print this
        if (not len(this) > 0): this = filter(lambda x: x[1] == next[0], edges)
        print this
        route.append(this[0])
        next = this[0]
        print "next",next
        edges.remove(this[0])

    print "connected:", route

    for i in xrange( len(route)-1):
        if route[i][1] !=  route[i+1][0]:
            route[i+1] = (route[i+1][1],route[i+1][0])

    flat_route = []
    for a_tuple in route:
        flat_route.extend(list(a_tuple))

    final_route = [flat_route[0]]
    for i in xrange(1,len(flat_route)):
        if (i%2==0):
            final_route.append(flat_route[i])

    print "FINAL: ",final_route
    return final_route






