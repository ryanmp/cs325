#Joshua Villwock, Ryan Phillips, Jaron Thatcher
#CS325: Analysis of Algotithms
#1/25/2014
#Implmentation Assignment 1

from random import shuffle
import time
import pylab
import timeit
import numpy as np
import cPickle as pickle
import sys


class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("log.dat", "a")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message) 
sys.stdout = Logger()

# large sets for timing
# 1k, 2k, 3k, 4k, 5k, 10k, 20k, 30k, 40k, 50k
n_vals = [1000,2000,3000,4000,5000,10000,20000,30000,40000,50000]

length = len(n_vals)

def gen_test_arr():
	test_arr = [[]*length for x in xrange(length)]
	for i in xrange(length):
		for j in xrange(length):
			temp = list(range(1,n_vals[j]))
			shuffle(temp)
			test_arr[i].append(temp)
	return test_arr


def brute_force(x):
	count = 0
	for i in range (0,len(x)):
		for j in range (i+1,len(x)):
			if x[i] > x[j]:
				count+=1
				#print(x[i],x[j]);
	return count

def naive_d_and_c(list_in):
	count = 0

	if len(list_in) < 2:
		return count

	middle = int(len(list_in)/2)

	left = list_in[:middle]
	right = list_in[middle:]

	for i in range (0,len(left)):
		for j in range (0,len(right)):
			if left[i] > right[j]:
				count += 1

	count += naive_d_and_c(left)
	count += naive_d_and_c(right)
	return count

# just a starter foo - it calls ms()
def merge_and_count(list_in):
	out = ms(list_in,0)
	return out[1]

# this is actually merge_and_count
def ms(x,count):
    results = []
    if len(x) < 2:
        return x, count
    mid = int(len(x)/2)
    l, count = ms(x[:mid],count)
    r, count = ms(x[mid:],count)
    i = 0
    j = 0
    while i < len(l) and j < len(r):
        if l[i] > r[j]:
            results.append(r[j])
            count += len(l) - i
            j += 1
        else:
            results.append(l[i])

            i += 1
    results += l[i:]
    results += r[j:]
    return results, count


def single_test(list,which,num_runs):
	if (which==0):
		timer1 = timeit.Timer(lambda: brute_force(list))
	elif (which==1):
		timer1 = timeit.Timer(lambda: naive_d_and_c(list))
	elif (which==2):
		timer1 = timeit.Timer(lambda: merge_and_count(list))
	average_time = timer1.timeit(num_runs) / num_runs
	print "avg of", num_runs, "trials: ", average_time
	return average_time


def test_timing(_verbose,which,test_arr):
	all_tests = []
	num_runs = 10 # max of 10
	for i in xrange(length):
		if _verbose:
			print "for length =", i, ":"
		time = single_test(test_arr[1][i],which,num_runs)
		all_tests.append(time)
	if _verbose:
		print all_tests
	return all_tests


def show_graphs(_results1,_results2,_results3,_n):

	_results1 = [0.03626370429992676, 0.1470473051071167, 0.33706371784210204, 0.6011320114135742, 0.9445984840393067, 3.846377897262573, 16.156464290618896, 37.681616806983946, 70.29044330120087, 115.75034708976746]
	_results2 = [0.03712019920349121, 0.14641458988189698, 0.33380799293518065, 0.5920280933380127, 0.9311999082565308, 3.780233311653137, 15.46792380809784, 36.150787115097046, 66.38889260292054, 107.12109808921814]
	_results3 = [0.003688812255859375, 0.007952690124511719, 0.012450504302978515, 0.01710178852081299, 0.022072505950927735, 0.047310400009155276, 0.10067009925842285, 0.15592021942138673, 0.21513760089874268, 0.2736771821975708]

	# plot raw data
	pylab.loglog(_n,_results1,'ro',basex=10,basey=10, label="brute force")
	pylab.loglog(_n,_results2,'bo',basex=10,basey=10, label="naive divide and conquer")
	pylab.loglog(_n,_results3,'go',basex=10,basey=10, label="merge and count")
	
	# add labels and legend
	pylab.xlabel('n')
	pylab.ylabel('Time (s)')
	pylab.legend(loc='lower right')

	# plot best fit lines for all 3 data sets
	slope,intercept=np.polyfit(np.log(_n),np.log(_results1),1)
	print "best-fit: [slope,intercept]",slope,intercept
	print "f() = ( e ^",intercept,") * n ^",slope
	t1 = np.arange(_n[0], _n[len(_n)-1], 0.01)
	s1 = (2.71828**intercept)*t1**slope
	pylab.loglog(t1, s1,'r',basex=10,basey=10,label='a')

	slope2,intercept2=np.polyfit(np.log(_n),np.log(_results2),1)
	print "best-fit: [slope,intercept]",slope2,intercept2
	print "f() = ( e ^",intercept2,") * n ^",slope2
	t2 = np.arange(_n[0], _n[len(_n)-1], 0.01)
	s2 = (2.71828**intercept2)*t2**slope2
	pylab.loglog(t2, s2,'b',basex=10,basey=10,label='b')

	slope3,intercept3=np.polyfit(np.log(_n),np.log(_results3),1)
	print "best-fit: [slope,intercept]",slope3,intercept3
	print "f() = ( e ^",intercept3,") * n ^",slope3
	t3 = np.arange(_n[0], _n[len(_n)-1], 0.01)
	s3 = (2.71828**intercept3)*t3**slope3
	pylab.loglog(t3, s3,'g',basex=10,basey=10,label='g')

	pylab.show()


def show_graphs2(_results1,_results2,_results3,_n):

	_results1 = [0.03626370429992676, 0.1470473051071167, 0.33706371784210204, 0.6011320114135742, 0.9445984840393067, 3.846377897262573, 16.156464290618896, 37.681616806983946, 70.29044330120087, 115.75034708976746]
	_results2 = [0.03712019920349121, 0.14641458988189698, 0.33380799293518065, 0.5920280933380127, 0.9311999082565308, 3.780233311653137, 15.46792380809784, 36.150787115097046, 66.38889260292054, 107.12109808921814]
	_results3 = [0.003688812255859375, 0.007952690124511719, 0.012450504302978515, 0.01710178852081299, 0.022072505950927735, 0.047310400009155276, 0.10067009925842285, 0.15592021942138673, 0.21513760089874268, 0.2736771821975708]

	pylab.xlabel('n')
	pylab.ylabel('Time (s)')
	pylab.legend(loc='lower right')

	pylab.plot(_n,_results1,'r', label="brute force")
	pylab.plot(_n,_results2,'g', label="brute force")
	pylab.plot(_n,_results3,'b', label="brute force")
	pylab.show()
	


def test_correctness1(_file):
	expected_values = []

	#convert verify.txt into a more friendly format
	f = open(_file)
	lines_raw = f.readlines()
	test_arr = []
	for i in range(0,len(lines_raw)):
		temp = []
		temp = lines_raw[i].split(',')
		temp = map(int, temp)
		expected_values.append(temp[len(temp)-1:])
		test_arr.append(temp[:len(temp)-1])

	failed_flag = False
	for i in range(0,len(lines_raw)):
		if (brute_force(test_arr[i]) == expected_values[i][0]):
			print "brute force passed:",i,brute_force(test_arr[i]),expected_values[i][0]
		else:
			print "brute force failed:",i,brute_force(test_arr[i]),expected_values[i][0] 

	for i in range(0,len(lines_raw)):
		temp_out = naive_d_and_c(test_arr[i])
		if (temp_out == expected_values[i][0]):
			print "naive_d_and_c passed:",i,naive_d_and_c(test_arr[i]),expected_values[i][0]
		else:
			print "naive_d_and_c failed:",i,naive_d_and_c(test_arr[i]),expected_values[i][0] 

	for i in range(0,len(lines_raw)):
		temp_out = merge_and_count(test_arr[i])
		if (temp_out == expected_values[i][0]):
			print "merge_and_count passed:",i,merge_and_count(test_arr[i]),expected_values[i][0]
		else:
			print "merge_and_count failed:",i,merge_and_count(test_arr[i]),expected_values[i][0] 

	if (failed_flag):
		return False
	else:
		return True


def test_correctness2(_file):

	results = []
	f = open(_file)
	lines_raw = f.readlines()
	test_arr = []
	for i in range(0,len(lines_raw)):
		temp = []
		temp = lines_raw[i].split(',')
		temp = map(int, temp)
		test_arr.append(temp)

	for i in range(0,len(lines_raw)):
		results.append(brute_force(test_arr[i]))
		results.append(naive_d_and_c(test_arr[i]))
		results.append(merge_and_count(test_arr[i]))

	return results
			

def main():


	print "generating many random inputs..."
	test_arr = gen_test_arr()

	'''
	if (test_correctness1("verify.txt")): print "passed all tests!"
	else: "failed correctness tests! Uh oh!" 

	results0 = test_correctness2('test_in.txt')
	print results0

	


	debug = True
	print 'timing brute force...'
	results1 = test_timing(debug,0,test_arr)
	print 'timing naive d & c...'
	results2 = test_timing(debug,1,test_arr)
	print 'timing merge & count...'
	results3 = test_timing(debug,2,test_arr)
	'''
	
	print 'saving results...'
	#pickle.dump( results1, open( "results1.p", "wb" ) )
	#pickle.dump( results2, open( "results2.p", "wb" ) )
	#pickle.dump( results3, open( "results3.p", "wb" ) )

	print 'loading results...'
	results1 = pickle.load( open( "results1.p", "rb" ) )
	results2 = pickle.load( open( "results2.p", "rb" ) )
	results3 = pickle.load( open( "results3.p", "rb" ) )

	print 'generating graphs...' 
	#show_graphs(results1,results2,results3,n_vals)

	show_graphs2(results1,results2,results3,n_vals)

main()
