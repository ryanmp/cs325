import timeit, random, itertools, pylab
import numpy as np
from brute_force import *
from div_and_conq import *
from dynamic_prog import *
import cPickle as pickle

# https://pypi.python.org/packages/source/g/guppy/guppy-0.1.10.tar.gz
# this is really unnecessary for this project
# just don't run the memory test and comment out the next line
from guppy import hpy

min_test = 1000
max_test = 10000
test_iter = 1000
num_trials = 10

#[algo][array_size][trial #]
# setting up our test result array
test_results = [[[1 for x in xrange(num_trials)] for x in range(min_test,max_test+min_test,test_iter)] for x in xrange(3)]

#for mem test
test_results2 = [[[1 for x in xrange(num_trials)] for x in range(min_test,max_test+min_test,test_iter)] for x in xrange(3)]


def test():
	for idx, x in enumerate(range(min_test,max_test+min_test,test_iter)):
		for y in xrange(num_trials):
			print 'testing',x,'trial',y
			t0 = [random.randint(-100,100) for r in xrange(x)]
			test_results[0][idx][y] = timeit.Timer(lambda: brute_force2(t0)).timeit(1)
			test_results[1][idx][y] = timeit.Timer(lambda: div_and_conq0(t0)).timeit(1)
			test_results[2][idx][y] = timeit.Timer(lambda: dynamic_prog0(t0)).timeit(1)


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


def show_graphs(test_results):

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

	print 'y-intercepts:', intercept, intercept2, intercept3
	print 'slopes:', slope, slope2, slope3

	pylab.legend(loc='upper left')

	#pylab.axis('tight')

	pylab.show()

# oh yeah, need a quick linear graph
def show_graphs2(test_results):

	# n values (input array sizes)
	_n = [[x for i in xrange(num_trials)] for x in range(min_test,max_test+min_test,test_iter)]
	_n = list(itertools.chain(*_n))

	# flatten 2d array
	_results1 = list(itertools.chain(*test_results[0]))
	_results2 = list(itertools.chain(*test_results[1]))
	_results3 = list(itertools.chain(*test_results[2]))


	pylab.plot(_n,_results1,'ro', label="Brute Force")
	pylab.plot(_n,_results2,'go', label="Divide & Conquer")
	pylab.plot(_n,_results3,'bo', label="Dynamic Programming")

	pylab.xlabel('n')
	pylab.ylabel('Time (s)')
	pylab.legend(loc='upper left')

	pylab.show()

# for mem usage
def show_graphs3(test_results2):

	# n values (input array sizes)
	_n = [[x for i in xrange(num_trials)] for x in range(min_test,max_test+min_test,test_iter)]
	_n = list(itertools.chain(*_n))

	# flatten 2d array
	_results1 = list(itertools.chain(*test_results2[0]))
	_results2 = list(itertools.chain(*test_results2[1]))
	_results3 = list(itertools.chain(*test_results2[2]))


	print _results1
	print _results2
	print _results3

	print _n

	pylab.xlabel('n')
	pylab.ylabel('mem usage (bytes)')

	pylab.ylim(150000, 200000)

	pylab.plot(_n,_results1, 'r', label="Brute Force")
	pylab.plot(_n,_results2, 'g', label="Divide & Conquer")
	pylab.plot(_n,_results3, 'b', label="Dynamic Programming")


	pylab.legend(loc='lower right')



	pylab.show()


def memory_tests():

	h = hpy()

	for idx, x in enumerate(range(min_test,max_test+min_test,test_iter)):
		for y in xrange(num_trials):
			print 'testing',x,'trial',y
			t0 = [random.randint(-100,100) for r in xrange(x)]

			h = hpy()
			h.setref()
			brute_force2(t0)
			hp = h.heap()
			total = 0
			for i in xrange(len(hp)):
				total += hp[i].size
				test_results2[0][idx][y] = total
			print total

			h = hpy()
			h.setref()
			div_and_conq0(t0)
			hp = h.heap()
			total = 0
			for i in xrange(len(hp)):
				total += hp[i].size
				test_results2[1][idx][y] = total
			print total

			h = hpy()
			h.setref()
			dynamic_prog0(t0)
			hp = h.heap()
			total = 0
			for i in xrange(len(hp)):
				total += hp[i].size
				test_results2[2][idx][y] = total
			print total

# comment/comment based on what tests you want to run
def main(test_results2):

	test_correctness('verify_2.txt')

	test() #performance tests
	pickle.dump( test_results, open( "results.p", "wb" ) ) #save
	#test_results = pickle.load( open( "results.p", "rb" ) ) #load
	show_graphs(test_results)
	#show_graphs2(test_results)

	#memory_tests()
	#pickle.dump( test_results2, open( "results_mem.p", "wb" ) )
	#test_results2 = pickle.load( open( "results_mem.p", "rb" ) )
	#show_graphs3(test_results2)

main(test_results2)



