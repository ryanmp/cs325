import sys, math

'''

from a starting city, it continually adds the next closest city to the route

'''

def algo_greedy(cities):
    route = [cities[0]]
    unvisited = cities[1:]
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

    return route2

