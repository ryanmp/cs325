'''

this is a great place to start:

http://nbviewer.ipython.org/url/norvig.com/ipython/TSPv3.ipynb



idea1:

okay, this one could probably be consider cheating, but I thought I'd include it here just for kicks.
we can safely assume that whatever we come up with won't be as efficient/powerful 
as that in a professional package, like say the TSP Solver that comes with mathematica.
So first we run the best existing TSP solver we can find to give us an idea of what we are shooting for.
Let's call this the Target Route.


Then we write our algos with a set of parameters that can be tweaked. We use the Target Route as our solution,
and solve for the parameters. Then we run our algo with these params, and tada! 

idea2:


'''



import math
import matplotlib
import matplotlib.pyplot as plt
import random
import time
import itertools
import timeit

random.seed('0')

def exact_TSP(cities):
    "Generate all possible tours of the cities and choose the shortest one."
    return shortest(alltours(cities))

def shortest(tours): 
    "Return the tour with the minimum total distance."
    return min(tours, key=total_distance)

def total_distance(tour):
	return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

City = complex # Constructor for new cities, e.g. City(300, 400)

def distance(A, B): return abs(A - B)

def Cities(n):
    return set(City(random.randrange(10, 890), random.randrange(10, 590)) for c in range(n))

def alltours(cities):
    "Return a list of tours, each a permutation of cities, but each one starting with the same city."
    start = first(cities)
    return [[start] + list(tour)
            for tour in itertools.permutations(cities - {start})]

def first(collection):
    "Start iterating over collection, and return the first element."
    for x in collection: return x

def greedy_TSP(cities):
    start = first(cities)
    tour = [start]
    unvisited = cities - {start}
    while unvisited:
        C = nearest_neighbor(tour[-1], unvisited)
        tour.append(C)
        unvisited.remove(C)
    return tour

def nearest_neighbor(A, cities):
    return min(cities, key=lambda x: distance(x, A))

def plot_tour(algorithm, cities):

    t0 = time.clock()
    tour = algorithm(cities)
    t1 = time.clock()
    
    plotline(list(tour) + [tour[0]])
    plotline([tour[0]], 'rs')
    plt.show()
    print("{} city tour; total distance = {:.1f}; time = {:.3f} secs for {}".format(
          len(tour), total_distance(tour), t1-t0, algorithm.__name__))
    
def plotline(points, style='bo-'):
    X, Y = XY(points)
    plt.plot(X, Y, style)
    
def XY(points):
    return [p.real for p in points], [p.imag for p in points]
    
#plot_tour(greedy_TSP, Cities(155))

# just a test
def my_min(n):
    print min([random.randrange(1,10000) for i in xrange(n)])
	

print timeit.Timer(lambda: my_min(int(1e6))).timeit(1)



