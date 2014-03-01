import tsp_grapher
import math, random, timeit, datetime

from functools import partial

from algo_exact import *
from algo_fastdumb import *
from algo_greedy import *

def parse_input(file_name):
	f = open(file_name)
	lines_raw = f.readlines()
	ret = []
	for i in range(0,len(lines_raw)):
		parsing_line = []
		parsing_line = lines_raw[i].split()
		parsing_line = map(int, parsing_line)
		to_tuple = (parsing_line[1],parsing_line[2])
		ret.append(to_tuple)
	return ret

def route_length(cities,route):
	distance = 0
	for i in xrange(len(route)-1):
		idx1 = route[i]
		idx2 = route[i+1]
		distance += math.hypot(cities[idx2][0] - cities[idx1][0], cities[idx2][1] - cities[idx1][1])
	return distance

def generate_test_set(_seed,_n,_range):
	random.seed(_seed)
	ret = []
	for i in xrange(_n):
		ret.append((random.randrange(1,_range),random.randrange(1,_range)))
	return ret

# { algorithm to test, range for n (n0=smallest -> n1=largest) }
def time_algo(f, n0, n1):
	ret = []
	for i in xrange(n0,n1):
		t1 = generate_test_set("0",i,100)
		ret.append(timeit.Timer(lambda: f(t1)).timeit(1))
	return ret, [i for i in range(n0,n1)], f

# { algorithm to test, range for n (n0=smallest -> n1=largest) }
def batch_algo_lengths(f, n0, n1):
	ret = []
	for i in xrange(n0,n1):
		t1 = generate_test_set("0",i,100)
		ret.append( route_length( t1, f(t1) ) )

	return ret, [i for i in range(n0,n1)], f

# not even close... need much better curve fitting, including exponential forms,
# and factorial too.. (rather than just linear {slope and intecept}) but I can't
# find such a thing...
def estimate_runtime(input_size, slope, intercept):
	out = (2.71828**intercept)*slope**input_size
	print str(datetime.timedelta(seconds=out))

#cities1 = parse_input("in/example-input-1.txt")
cities1 = generate_test_set("0",9,200)

'''

route = algo_greedy(cities1)
tsp_grapher.plot_route(cities1,route)
print route_length(cities1, route), route

route = algo_exact(cities1)
tsp_grapher.plot_route(cities1,route)
print route_length(cities1, route), route

route = algo_fastdumb(cities1)
tsp_grapher.plot_route(cities1,route)
print route_length(cities1, route), route

'''

n0 = 2
n1 = 240

#l1, r1, f1 = batch_algo_lengths(algo_exact,n0,n1) #doesn't like a list of just one city
l2, r2, f2 = batch_algo_lengths(algo_greedy,n0,n1)
l3, r3, f3 = batch_algo_lengths(algo_fastdumb,n0,n1)
tsp_grapher.plot_lengths([l2,l3], [r2,r3], [f2,f3])

#t1, r1, f1 =  time_algo(algo_exact,n0,n1)
t2, r2, f2 =  time_algo(algo_greedy,n0,n1)
t3, r3, f3 =  time_algo(algo_fastdumb,n0,n1)
slopes, intercepts = tsp_grapher.plot_timing([t2,t3],[r2,r3],[f2,f3])
#estimate_runtime(11,slopes[0],intercepts[0]) 








