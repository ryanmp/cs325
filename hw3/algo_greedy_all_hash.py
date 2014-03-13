import sys, math
from helpers import *

'''

from a starting city, it continually adds the next closest city to the route

this algo on average should return shorter routes than algo_greedy since it runs algo_greedy
on every possible start city.

But the trade off is that it's slower by a factor of n.

'''

def algo_greedy_all_hash(cities,dict_distances):

    shortest_route_dist = sys.maxint
    best_route = []

    # doing this globally...
    '''
    dict_distances = {}
    for idx1 in xrange(len(cities)):
        for idx2 in range(idx1,len(cities)):
            if (idx1 != idx2):
                dict_distances[str(cities[idx1])+str(cities[idx2])] = distance(cities[idx1],cities[idx2])
    '''

    for i in xrange(0,len(cities)-1):
        route = [cities[i]]
        unvisited = cities[:i+0] + cities[i+1:]

        while unvisited:
            closest_dist = sys.maxint
            closest_idx = 0
            for i in unvisited:
                
                # ouch look at the format of that key
                k1 = '('+str(i[0])+', '+str(i[1])+')('+str(route[-1][0])+', '+str(route[-1][1])+')'
                k2 = '('+str(route[-1][0])+', '+str(route[-1][1])+')('+str(i[0])+', '+str(i[1])+')'
                # two possible orderings: city1, city2 or city2, city1
                try:
                    distance1 = dict_distances[k1]
                except:
                    distance1 = dict_distances[k2]

                if distance1 < closest_dist:
                    closest_dist = distance1
                    closest_idx = i
            route.append(closest_idx)
            unvisited.remove(closest_idx)

        route2 = []
        for i in route:
            route2.append(cities.index(i))

        test_length = route_length_hash(cities,route2,dict_distances)

        if (test_length < shortest_route_dist):
            shortest_route_dist = test_length
            best_route = route2

    return best_route

