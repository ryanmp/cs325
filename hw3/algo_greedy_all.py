import sys, math

from helpers import *

'''

from a starting city, it continually adds the next closest city to the route

'''

def algo_greedy_all(cities):

    shortest_route_dist = sys.maxint
    best_route = []

    for i in xrange(0,len(cities)-1):
        route = [cities[i]]
        unvisited = cities[:i+0] + cities[i+1:]

        while unvisited:
            closest_dist = sys.maxint
            closest_idx = 0
            for i in unvisited:
                distance = math.hypot(i[0] - route[-1][0], i[1] - route[-1][1])
                if distance < closest_dist:
                    closest_dist = distance
                    closest_idx = i
            route.append(closest_idx)
            unvisited.remove(closest_idx)

        route2 = []
        for i in route:
            route2.append(cities.index(i))

        test_length = route_length(cities,route2)

        if (test_length < shortest_route_dist):
            shortest_route_dist = test_length
            best_route = route2

    return best_route

