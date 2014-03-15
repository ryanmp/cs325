import sys, math, itertools
from helpers import *
from operator import itemgetter

from algo_greedy import *

'''
uses algo_greedy on subsets of city (broken up via a grid),
then uses algo_greedy on the average center of these subsets to decide how to put them back together
additionally it tries every rotation/reversal when recombining the subsets

'''

def algo_greedy_segmented(cities):

    #how many divisions should we use??
    #the success of this algorithm is largely dependent on these values,
    #but i have no clue how to pick the proper 
    #number of divions for an input
    grid_div_x = 30
    grid_div_y = 30

    villages = [[[] for i in xrange(grid_div_y)] for i in xrange(grid_div_x)]
    village_routes = []
    village_centers = []

    x_min = min(cities,key=itemgetter(0))[0]
    y_min = min(cities,key=itemgetter(1))[1]
    x_max = max(cities,key=itemgetter(0))[0]
    y_max = max(cities,key=itemgetter(1))[1]

    for x in xrange(0, len(cities)):

        for i in xrange(grid_div_x):
            for j in xrange(grid_div_y):

                if cities[x][0] >= (float(i)/grid_div_x)*x_max and cities[x][0] <= ((float(i)+1)/grid_div_x)*x_max:
                    if cities[x][1] >= (float(j)/grid_div_y)*y_max and cities[x][1] <= ((float(j)+1)/grid_div_y)*y_max:
                        villages[i][j].append(cities[x])

    #unwrap nested array
    villages = list(itertools.chain(*villages))

    for v in villages:
        
        #get approximate center of village
        if (len(v) > 0):
            x_center = 0.0
            y_center = 0.0
            for i in v:
                x_center += i[0]
                y_center += i[1]
            x_center = x_center/len(v)
            y_center = y_center/len(v)
            village_centers.append( (x_center,y_center) )

            # run greedy on village
            temp = algo_greedy(v)

            # convert village index back to city index
            village_route = []
            for idx in xrange(len(temp)):
                village_route.append( cities.index( v[temp[idx]] ))
            village_routes.append(village_route)

    '''

    # this is waaaay too slow

    # recombine subroutes into every possible complete route
    all_permutations = list(itertools.permutations(village_routes))
    all_p = []
    for p in all_permutations:
        all_p.append( list(itertools.chain.from_iterable(p)) )

    # compare all these possible complete routes
    shortest_route_dist =  sys.maxint
    best_route = []
    for p in all_p:
        test_length = route_length(cities,p)
        if (test_length < shortest_route_dist):
            shortest_route_dist = test_length
            best_route = p

    return best_route
    '''

    shortest_route_dist =  sys.maxint

    ret = []

    #print village_routes

    # we need to recombine these sub routes in a smarter way(by avg location perhaps?)
    #ret = list(itertools.chain(*village_routes))

    # run greedy on village centers
    temp = algo_greedy(village_centers)

    for i in temp:
        tmp = village_routes[i]
        ret.append(tmp)

    ret2 = list(itertools.chain(*ret))
    default_distance = route_length(cities,ret2)

    for idx1 in xrange(len(temp)):
        for i in range(0,len(ret[idx1])):
            for j in range(2):
                revert = ret[idx1]
                ret[idx1] = ret[idx1][i:] + ret[idx1][:i]
                if (j == 1): ret[idx1].reverse()
                ret3 = list(itertools.chain(*ret))
                new_distance = route_length(cities,ret3)
                if new_distance > default_distance:
                    ret[idx1] = revert
    
    ret4 = list(itertools.chain(*ret))

    return ret4

