import tsp_grapher
import random, timeit, datetime, time

from functools import partial

from algo_exact import *
from algo_fastdumb import *
from algo_greedy import *
from algo_greedy_all import *
from algo_inverse_prim import *

from helpers import *

n0 = 3    #Minimum input size to try
n1 = 80    #Maximum input size to try

def generate_test_set(_n,_range):
	global set
	random.seed("0")    #Seeds the RNG.  This causes us to use the same test set every run.
	set = []
	for i in xrange(_n):
		set.append((random.randrange(1,_range),random.randrange(1,_range)))
	return set

def return_set(max):
	global set
	#not done
	return set[:max]

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

# { algorithm to test, range for n (n0=smallest -> n1=largest) }
def time_algo(f, n0, n1):
	ret = []
	for i in xrange(n0,n1):
		t1 = return_set(i)
		ret.append(timeit.Timer(lambda: f(t1)).timeit(1))
	return ret, [i for i in range(n0,n1)], f

# { algorithm to test, range for n (n0=smallest -> n1=largest) }
def batch_algo(f, n0, n1):
	ret = []
	timings = []
	for i in xrange(n0,n1):
		t1 = return_set(i)
		start_time = time.time()
		ret.append( route_length( t1, f(t1) ) )
		timings.append(time.time()-start_time)

	return ret, [i for i in range(n0,n1)], f, timings

# just a quicker way to call batch_algo_lengths on multiple algos...
#{ algo_name_1, algo_name2, ... }
def batch_compare_algos(*arg):
	lengths = []
	ranges = []
	f_names = []
	all_times = []
	for i in arg:
		l0, r0, f0, t0= batch_algo(i,n0,n1)
		lengths.append(l0)
		ranges.append(r0)
		f_names.append(f0)
		all_times.append(t0)
	tsp_grapher.plot_lengths(lengths, ranges, f_names)
	tsp_grapher.plot_timing(all_times, ranges, f_names)

#{ number of cities, [algo1, algo2, etc] }
def compare_algos(_n, _algos):
	cities0 = return_set(_n)
	all_routes = []
	for _algo in _algos:
		all_routes.append(_algo(cities0))
	tsp_grapher.plot_routes(cities0,all_routes)

# not even close... need much better curve fitting, including exponential forms,
# and factorial too.. (rather than just linear {slope and intecept}) but I can't
# find such a thing...
def estimate_runtime(input_size, slope, intercept):
	out = (2.71828**intercept)*slope**input_size
	print str(datetime.timedelta(seconds=out))


def main():

	#initialize random inputs:
	generate_test_set(n1,100)

	# this will plot route_length vs. N & 
	# timing vs. N for each algorithm listed
	# (using the default range+seed declared up in the global variable)
	batch_compare_algos(algo_greedy,algo_greedy_all)

	# this will plot the resultant route from each algorithm for
	# a given city set size (using the default seed)
	compare_algos(25,[algo_greedy,algo_greedy_all])

	'''
	#cities1 = parse_input("in/example-input-1.txt")
	cities1 = return_set(9)

	route = algo_greedy(cities1)
	tsp_grapher.plot_route(cities1,route)
	print route_length(cities1, route), route
	'''

main()
