import sys, math

'''

from a starting city, it continually adds the next closest city to the route

'''

def algo_greedy_all(cities):

    shortest_route_so_far = sys.maxint

    for i in xrange(0,len(cities)):

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

        test_length = route_length2(cities,route2)
        if (test_length < shortest_route_so_far):
            shortest_route_so_far = test_length

    return route2


def route_length2(cities,_route):
    distance = 0
    for i in xrange(len(_route)-1):
        idx1 = _route[i]
        idx2 = _route[i+1]
        distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])
    return distance
