import timeit, random, itertools, pylab
import numpy as np
from brute_force import *
from div_and_conq import *
from dynamic_prog import *

# test cases
t1 = [31,-41,59,26,-53,58,97,-93,-23,84] # 187
t2 = [random.randint(-100,100) for r in xrange(10)]


min_test = 10
max_test = 5010
test_iter = 500

num_trials = 1

#[algo][array_size][trial #]
# setting up our test result array
test_results = [[[1 for x in xrange(num_trials)] for x in range(min_test,max_test+min_test,test_iter)] for x in xrange(3)]

def test():
	for idx, x in enumerate(range(min_test,max_test+min_test,test_iter)):
		for y in xrange(num_trials):
			print 'testing',x,'trial',y
			t0 = [random.randint(-100,100) for r in xrange(x)]
			test_results[0][idx][y] = timeit.Timer(lambda: brute_force2(t0)).timeit(1)
			test_results[1][idx][y] = timeit.Timer(lambda: div_and_conq0(t0)).timeit(1)
			test_results[2][idx][y] = timeit.Timer(lambda: dynamic_prog0(t0)).timeit(1)

def show_graphs():

	# n values (input array sizes)
	_n = [[x for i in xrange(num_trials)] for x in range(min_test,max_test+min_test,test_iter)]
	_n = list(itertools.chain(*_n))

	# flatten 2d array
	_results1 = list(itertools.chain(*test_results[0]))
	_results2 = list(itertools.chain(*test_results[1]))
	_results3 = list(itertools.chain(*test_results[2]))

	# plot raw data
	pylab.loglog(_n,_results1,'ro',basex=10,basey=10, label="Brute Force")
	pylab.loglog(_n,_results2,'bo',basex=10,basey=10, label="Divide & Conquer")
	pylab.loglog(_n,_results3,'go',basex=10,basey=10, label="Dynamic Programming")
	
	# add labels and legend
	pylab.xlabel('n')
	pylab.ylabel('Time (s)')
	

	# plot best fit lines for all 3 data sets
	slope,intercept=np.polyfit(np.log(_n),np.log(_results1),1)
	t1 = np.arange(_n[0], _n[len(_n)-1], 0.01)
	s1 = (2.71828**intercept)*t1**slope
	pylab.loglog(t1, s1,'r',basex=10,basey=10,label='')

	slope2,intercept2=np.polyfit(np.log(_n),np.log(_results2),1)
	t2 = np.arange(_n[0], _n[len(_n)-1], 0.01)
	s2 = (2.71828**intercept2)*t2**slope2
	pylab.loglog(t2, s2,'b',basex=10,basey=10,label='')

	slope3,intercept3=np.polyfit(np.log(_n),np.log(_results3),1)
	t3 = np.arange(_n[0], _n[len(_n)-1], 0.01)
	s3 = (2.71828**intercept3)*t3**slope3
	pylab.loglog(t3, s3,'g',basex=10,basey=10,label='')

	print slope, slope2, slope3

	pylab.legend(loc='upper left')

	#pylab.axis('tight')

	pylab.show()

def main():
	test()
	show_graphs()

#main()

def test_correctness(_file):
	expected_values = []

	#convert verify.txt into a more friendly format
	f = open(_file)
	lines_raw = f.readlines()
	test_arr = []
	for i in range(0,len(lines_raw)):
		temp = []
		temp = lines_raw[i].split(',')
		temp = map(int, temp)
		expected_values.append(temp[len(temp)-1])
		test_arr.append(temp[:len(temp)-1])

	for i in xrange(len(expected_values)):
		out = brute_force2(test_arr[i])
		#print out, expected_values[i]
		assert(out == expected_values[i])
		out = div_and_conq0(test_arr[i])
		#print out, expected_values[i]
		assert(out == expected_values[i])
		out = dynamic_prog0(test_arr[i])
		#print out, expected_values[i]
		assert(out == expected_values[i])

	print "passed all tests!"

test_correctness('verify_2.txt')
