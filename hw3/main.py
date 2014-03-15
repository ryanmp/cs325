'''

test1
the last stage of improvements was exact n=8

test2
to beat: 127149.005328

'''


import timeit, datetime, time, os
from functools import partial

#these work properly
from algo_exact import *
from algo_fastdumb import *
from algo_greedy import *
from algo_greedy_all import *

#and these do not
from algo_greedy_segmented import *
from algo_inverse_prim import *

#improve upon an existing route
from algo_improve_rev import *
from algo_improve_rev_wrap import *
from algo_improve_swap import *
from algo_improve_exact_segment import *

from tree import * #basic tree data structure
from algo_mst import * 

from helpers import *
import tsp_grapher

#import tsp-verifier #naming convention error!

n0 = 5 #Minimum input size to try
n1 = 50	#Maximum input size to try

def generate_test_set(_n,_range):
	global set
	random.seed("3r3")    #Seeds the RNG.  This causes us to use the same test set every run.
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

	#t1 = generate_test_set2("ok",n1,1000)

	for i in xrange(n0,n1):
		print i
		t2 = return_set(i)

		#t2 = t1[:n1]

		start_time = time.time()
		ret.append( route_length( t2, f(t2) ) )
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
	#cities0 = return_set(_n)

	cities0 = generate_test_set2("ok",_n,1000)

	all_routes = []
	for _algo in _algos:
		all_routes.append(_algo(cities0))
	for i in all_routes:
		print route_length(cities0,i)

	tsp_grapher.plot_routes(cities0,all_routes)

# not even close... need much better curve fitting, including exponential forms,
# and factorial too.. (rather than just linear {slope and intecept}) but I can't
# find such a thing...
def estimate_runtime(input_size, slope, intercept):
	out = (2.71828**intercept)*slope**input_size
	print str(datetime.timedelta(seconds=out))

def generate_test_set2(_seed,_n,_range):
	random.seed(_seed)
	ret = []
	for i in xrange(_n):
		ret.append((random.randrange(1,_range),random.randrange(1,_range)))
	return ret

def format_output(cities, route, file_name):
	#create a file
	f = open(file_name, "wb")

	#first line is the route length as an int
	#i'm using a new route_length function, because tsp-verifier needs
	#a lot of rounding
	route_length_str = str(int(route_length_final(cities,route)))+"\n"
	f.write(route_length_str)

	#write each city in route as new line
	for i in route:
		f.write(str(i)+"\n")
	f.close()

def run_verifier(cities_txt,route_txt):
	path = os.getcwd() + "/"
	os.system("python tsp-verifier.py "+path+cities_txt+" "+path+route_txt)

def algo_combo1(cities):
	route = algo_fastdumb(cities)
	for i in xrange(int(len(cities)/2),len(cities)):
		route = algo_improve_rev_wrapper(cities,route,i)
	return route
	
def algo_combo2(cities):
	route = algo_fastdumb(cities)
	for i in xrange(int(len(cities)/2),len(cities)):
		route = algo_improve_rev_old(cities,route,i)
	return route

def read_route(file_name):
	f = open(file_name)
	lines_raw = f.readlines()
	lines_raw = lines_raw[1:]
	ret = []
	for i in range(0,len(lines_raw)):
		ret.append(int(lines_raw[i]))
	return ret

def compare_improvements(route,cities,max):

	times = []
	lengths = []
	iterations = []
	idx = 0

	start_time = time.time()
	times.append(time.time() - start_time)
	lengths.append(route_length(cities,route))
	iterations.append(idx)

	while (time.time() - start_time < max):
	#while idx < max:


		for x in xrange(random.randint(1,6)):
			idx += 1
			for i in xrange(2,len(cities)):
				route = algo_improve_rev(cities,route,i)
			print route_length(cities,route) 
			times.append(time.time() - start_time)
			lengths.append(route_length(cities,route))
			iterations.append(idx)

		for i in xrange(2,len(cities)):
			idx += 1
			route = algo_improve_rev(cities,route,i)

			if (random.random() < .01):
				route = algo_improve_rev(cities,route,i)
				print route_length(cities,route) 
				idx += 1
			print route_length(cities,route) 
			times.append(time.time() - start_time)
			lengths.append(route_length(cities,route))
			iterations.append(idx)

		'''	
		for i in xrange(10,len(cities)):
			idx += 1
			route = algo_improve_exact_segment(cities,route,i-7,i)
			print route_length(cities,route) 
			times.append(time.time() - start_time)
			lengths.append(route_length(cities,route))
			iterations.append(idx)
		'''
		
		
		

	tsp_grapher.plot_improvements([iterations],[lengths],len(cities))
	return route


def main():

	#initialize random inputs:
	#generate_test_set(n1,1000)

	# this will plot route_length vs. N & 
	# timing vs. N for each algorithm listed
	# (using the default range+seed declared up in the global variable)
	#batch_compare_algos(algo_combo1,algo_combo2)

	# this will plot the resultant route from each algorithm for
	# a given city set size (using the default seed)
	#compare_algos(15,[algo_combo1,algo_combo1])

	'''
	cities = return_set(10)
	route = algo_fastdumb(cities)
	route = algo_improve_rev(cities,route,3)
	print route
	'''

	#generate_test_set(n1,1000)




	cities = parse_input("test2.txt")

	route = read_route("t2_better4")

	tsp_grapher.plot_route(cities,route)

	'''
	for i in xrange(6,len(cities)):
		route = algo_improve_exact_segment(cities,route,i-6,i)
		print route_length(cities,route), i
	
	format_output(cities, route, "tmp")
	run_verifier("test2.txt","tmp")
	'''






	#route2 = compare_improvements(route2,cities,2)
	#tsp_grapher.plot_route(cities,route)
	#format_output(cities, route2, "test1")
	#run_verifier("test1.txt","test1")

	'''
	route = algo_improve_swap(cities,route)

	for i in xrange(2,len(cities)):
		route = algo_improve_rev(cities,route,i)
		print route_length(cities,route)
	'''
	



	

	'''
	for i in xrange(2,int(len(citis)/3)):
		route = algo_improve_rev(cities,route,i)
		print route_length(cities,route)
		'''
	'''
	print route_length(cities,route)
	tsp_grapher.plot_route(cities,route)
	format_output(cities, route, "t1_mst.txt")
	run_verifier("test1.txt","t1_mst.txt")
	'''


	#run_verifier("test1.txt","t1g_all.txt")

	#route2 = read_route("out/example-output-3.txt")
	#tsp_grapher.plot_route(cities,route2)

	#print route
	#route = algo_improve_exact_segment(cities,route,10,16)
	#print route

	#route = [0,0,1,2,3]
	#print is_valid(cities1,route)
	'''

	#format_output(cities1, route, "out.txt")
	#run_verifier("in/example-input-1.txt","out.txt")

	#print route_length(cities1, route)
	#tsp_grapher.plot_route(cities1,route)


	route = algo_greedy_all(cities1)
	#tsp_grapher.plot_route(cities1,route)
	print "greedy_all results:", route_length(cities1, route)
	for i in xrange(2,len(cities1)):
		route = algo_improve_rev(cities1,route,i)
	print "results after improvements:", route_length(cities1, route)
	#tsp_grapher.plot_route(cities1,route)

	route = algo_mst(cities1)
	#tsp_grapher.plot_route(cities1,route)
	print "mst results:", route_length(cities1, route)
	for i in xrange(2,len(cities1)):
		route = algo_improve_rev(cities1,route,i)
	print "results after improvements:", route_length(cities1, route)
	#tsp_grapher.plot_route(cities1,route)
	'''
	

main()



