import timeit, random
from brute_force import *

t1 = [31,-41,59,26,-53,58,97,-93,-23,84] # 187
t2 = [random.randint(-100,100) for r in xrange(10)]
t3 = [1,3,5,7,11]

def test(n,l):
	arr_len = l
	out0 = 0
	'''
	#this one is stupidly slow which is why i have it commented out
	for i in xrange(n): #500 trials
		t0 = [random.randint(-100,100) for r in xrange(arr_len)] # randomize each time
		out0 += timeit.Timer(lambda: brute_force0(t0)).timeit(1)
	'''
	out1 = 0
	for i in xrange(n): #500 trials
		t0 = [random.randint(-100,100) for r in xrange(arr_len)] # randomize each time
		out1 += timeit.Timer(lambda: brute_force1(t0)).timeit(1)
	out2 = 0
	for i in xrange(n): #500 trials
		t0 = [random.randint(-100,100) for r in xrange(arr_len)] # randomize each time
		out2 += timeit.Timer(lambda: brute_force2(t0)).timeit(1)
	print out0,out1,out2



