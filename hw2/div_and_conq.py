import sys

'''
author: Ryan Phillips
solves the max subarray problem with a divide and conquer algo
'''

def div_and_conq0(x):

	max_sum = -sys.maxint - 1;

	def inner(x,max_sum):

		# base case
		if (len(x) <= 2):
			if sum(x) > max_sum:
				max_sum = sum(x)
			return max_sum

		mid = int(len(x)/2)
		l = x[:mid]
		r = x[mid:]

		# is left half max?
		new_sum_l = sum(l)
		max_sum = max(max_sum, new_sum_l)

		# is right half max?
		new_sum_r = sum(r)
		max_sum = max(max_sum, new_sum_r)



		# does it cross the mid?
		suffix_sum = 0
		max_suffix_sum = 0
		for i in range(mid-1,-1,-1):
			suffix_sum += x[i]
			max_suffix_sum = max(max_suffix_sum, suffix_sum)

		prefix_sum = 0
		max_prefix_sum = 0
		for i in range(mid,len(x)):
			prefix_sum += x[i]
			max_prefix_sum = max(max_prefix_sum, prefix_sum)

		max_sum = max(max_sum, max_suffix_sum + max_prefix_sum)

		# recursive calls
		ret = inner(l,max_sum) 
		if (ret != None):
			max_sum = max(ret,max_sum)

		ret = inner(r,max_sum)	
		if (ret != None):
			max_sum = max(ret,max_sum)	

		# end of inner_foo
		return max_sum

	ret = inner(x,max_sum)
	if (ret != None):
		max_sum = max(ret,max_sum)

	return max_sum








