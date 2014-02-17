import sys

'''
author: Ryan Phillips
solves the max subarray problem by brute force
'''

def brute_force0(x): 
	max_sum = -sys.maxint - 1;
	for i in xrange(len(x)):
		for j in range(i,len(x)):
			new_sum = sum(x[i:j])
			if new_sum > max_sum:
				max_sum = new_sum
	return max_sum # wait... this might not be correct (try t3)

# i think this one most closely matches  
# project description 
#
# it's always faster than brute_force0
def brute_force1(x): 
	max_sum = -sys.maxint - 1;
	l = len(x)
	for i in xrange(l):
		new_sum = 0
		for j in range(i,l):
			new_sum += x[j] 
			if new_sum > max_sum:
				max_sum = new_sum
	return max_sum

# faster than brute_force1 when input array length is > 350
def brute_force2(x): 
	max_sum = -sys.maxint - 1;
	l = len(x)
	new_sum = 0
	sums = [0 for r in xrange(l)]
	for i in xrange(l):
		new_sum += x[i] 
		sums[i] = new_sum
		if new_sum > max_sum: max_sum = new_sum
		sum2 = sums[i]
		for j in range(0,i-1):
			sum2 -= x[j]
			if sum2 > max_sum: max_sum = sum2
	return max_sum