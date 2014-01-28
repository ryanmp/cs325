from random import shuffle
import time
import matplotlib.pyplot as plt
import pylab
import numpy as np
import cPickle as pickle

basic_arr = [4,2,5,3,1,8];
#should yield 7

#large sets for timing
#1k, 2k, 3k, 4k, 5k, 10k, 20k, 30k, 40k, 50k
n_vals = [1000,2000,3000,4000,5000,
		10000,20000,30000,40000,50000]
n_vals2 = [100,200,300,400,500,600,700,800,900,1000]

# brute force times on my comp?
# 10k ~ 9s
# 20k ~ 40s
# 30k ~ 116s
# 40k ~ hell no...
# 50k ~ 

length = len(n_vals) #or n_vals

test_arr = [[]*length for x in xrange(length)]
def gen_test_arr():
	print "generating random inputs"
	for i in xrange(length):
		for j in xrange(length):
			temp = list(range(1,n_vals[j]))
			shuffle(temp)
			test_arr[i].append(temp)
	print "input array populated!"

# using smaller values during development,
# otherwise it takes way too damn long
test_arr2 = [[]*length for x in xrange(length)]
def gen_test_arr2():
	print "generating random inputs"
	for i in xrange(length):
		for j in xrange(length):
			temp = list(range(1,n_vals2[j]))
			shuffle(temp)
			test_arr2[i].append(temp)
	print "input array populated!"

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

	# base case
	if len(list_in) < 2:
		return count

	middle = int(len(list_in)/2)

	# recursive calls
	left = list_in[:middle]
	right = list_in[middle:]

	for i in range (0,len(left)):
		for j in range (0,len(right)):
			if left[i] > right[j]:
				count += 1
				#print left[i], right[j]

	#print count

	count += naive_d_and_c(left)
	count += naive_d_and_c(right)

	return count

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
                #print l,r
                #print(count)

                j += 1
            else:
                results.append(l[i])

                i += 1
    results += l[i:]
    results += r[j:]
    return results, count

def single_test(x,which):
	start_time = time.time()
	if (which==0):
		brute_force(x)
	elif (which==1):
		naive_d_and_c(x)
	elif (which==2):
		merge_and_count(x)
	end_time = time.time()
	elapsed_time = end_time - start_time
	return elapsed_time

def test_timing(_verbose,which):
	all_tests = []
	for i in xrange(10): #10 trials for a given n-value
		times = [] 
		if _verbose:
			print "for n =", n_vals[i] 
		for j in xrange(length):
			single_time = single_test(test_arr[j][i],which)
			if _verbose:
				print single_time
			times.append(single_time)
		average = (sum(times) / float(len(times)))
		if _verbose:
			print "avg of 10 trials: ", average 
		all_tests.append(average)
		#end 10 trials

	if _verbose:
		print all_tests
	return all_tests

def show_graphs(_results1,_results2,_results3,_n):

	pylab.xlabel('n')
	pylab.ylabel('Time (s)')

	#plot data
	pylab.loglog(_n,_results1,'ro',basex=10,basey=10, label="brute force")
	pylab.loglog(_n,_results2,'bo',basex=10,basey=10, label="naive divide and conquer")
	pylab.loglog(_n,_results3,'go',basex=10,basey=10, label="merge and count")
	
	pylab.legend(loc='lower right')

	# plot best fit poly foo
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

def test_correctness():
	expected_values = []
	f = open("verify.txt")
	lines = f.readlines()
	lines2 = []
	for i in range(0,len(lines)):
		temp = []
		temp = lines[i].split(',')
		temp = map(int, temp)
		expected_values.append(temp[len(temp)-1:])
		lines2.append(temp[:len(temp)-1])

	failed_flag = False
	for i in range(0,len(lines)):
		if (brute_force(lines2[i]) == expected_values[i][0]):
			print "brute force passed:",i,brute_force(lines2[i]),expected_values[i][0]
		else:
			print "brute force failed:",i,brute_force(lines2[i]),expected_values[i][0] 

	for i in range(0,len(lines)):
		temp_out = naive_d_and_c(lines2[i])
		if (temp_out == expected_values[i][0]):
			print "naive_d_and_c passed:",i,naive_d_and_c(lines2[i]),expected_values[i][0]
		else:
			print "naive_d_and_c failed:",i,naive_d_and_c(lines2[i]),expected_values[i][0] 

	for i in range(0,len(lines)):
		temp_out = merge_and_count(lines2[i])
		if (temp_out == expected_values[i][0]):
			print "merge_and_count passed:",i,merge_and_count(lines2[i]),expected_values[i][0]
		else:
			print "merge_and_count failed:",i,merge_and_count(lines2[i]),expected_values[i][0] 

	if (failed_flag):
		print "FAILED TESTS!"
	else:
		print "Passed All Tests!"

def main():

	# tests against verify.txt (contains many lists of numbers
	# followed by the number of inversion in the list)
	# test_correctness()

	# generates large arrays... results contains list of "time for execution"
	gen_test_arr()

	#False = no debug print statements
	# 0 = which -> brute, naive, or mergesort
	debug = True

	'''
	print 'timing1...'
	results1 = test_timing(debug,0)
	pickle.dump( results1, open( "results1.p", "wb" ) )
	print 'timing2...'
	results2 = test_timing(debug,1)
	pickle.dump( results2, open( "results2.p", "wb" ) )
	print 'timing3...'
	results3 = test_timing(debug,1)
	pickle.dump( results3, open( "results3.p", "wb" ) )
	''' 

	results1 = pickle.load( open( "results1.p", "rb" ) )
	results2 = pickle.load( open( "results2.p", "rb" ) )
	results3 = pickle.load( open( "results3.p", "rb" ) )

	#print results1
	#print results2
	#print results3

	# remember for graphing & analysis, the n-vals that were used can be found at "n_vals" 
	show_graphs(results1,results2,results3,n_vals)

	#return results1, results2
