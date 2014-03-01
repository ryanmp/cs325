import tsp_grapher
import math, random

from algo_exact import *
from algo_fastdumb import *

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

#cities1 = parse_input("in/example-input-1.txt")
cities1 = generate_test_set("0",8,200)

route = algo_exact(cities1)
tsp_grapher.plot_route(cities1,route)
print route_length(cities1, route), route

route = algo_fastdumb(cities1)
tsp_grapher.plot_route(cities1,route)
print route_length(cities1, route), route






