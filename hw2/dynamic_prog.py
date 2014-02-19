
'''
author: Ryan Phillips
solves the max subarray problem via dynamic programming
'''

def dynamic_prog0(x):

    this_sub_arr_sum = 0 
    max_sum = 0
    
    for i in x:

    	# print this_sub_arr_sum
    			
    	# does adding the last element make it bigger?
    	if this_sub_arr_sum + i > 0: 
    		this_sub_arr_sum = this_sub_arr_sum + i
    	else:
    		# failed to make a larger array so we are starting over 
    		# at the new idx
    		this_sub_arr_sum = 0

    	if this_sub_arr_sum > max_sum:
    		max_sum = this_sub_arr_sum

    return max_sum
			
