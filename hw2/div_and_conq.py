import sys

'''
author: Ryan Phillips
solves the max subarray problem with a divide and conquer algo
'''

# currently slower than brute_force ...
# that can't be right
def div_and_conq0(x):

	max_sum = -sys.maxint - 1;

	def inner(x,max_sum):

		# base case
		if (len(x) <= 1):
			if x > max_sum:
				max_sum = x
			return max_sum

		mid = int(len(x)/2)
		l = x[mid:]
		r = x[:mid]

		# is left half max?
		new_sum = sum(l)
		if new_sum > max_sum: max_sum = new_sum

		# is right half max?
		new_sum = sum(r)
		if new_sum > max_sum: max_sum = new_sum

		# does it cross the mid?
		for i in range(0,mid):
			for j in range(mid,len(x)):
				new_sum = sum(x[i:j])
				if new_sum > max_sum: max_sum = new_sum

		# recursive calls
		ret = inner(l,max_sum) 
		if (ret != None):
			max_sum = ret

		ret = inner(r,max_sum)	
		if (ret != None):
			max_sum = ret		

		# end of inner_foo
		return max_sum

	ret = inner(x,max_sum)
	if (ret != None):
		max_sum = ret	

	return max_sum