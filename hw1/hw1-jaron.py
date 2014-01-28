import math
import random

merge_count = 0 #counter variable for the number of inversions in the merge_and_count algorithm


def brute_force(array):
    #finds the merge_count in an array of integers using a brute force approach

    count = 0 #counter variable for the number of inversions

    for i in range (0, len(array)):
        temp = array[i]
        for j in range (i, len(array)):
            if temp > array[j]:
                count += 1

    return count


def div_and_conq(array):
    #finds the merge_count in an array of ints using a naive divide and conquer approach
    
    count = 0

    if len(array) == 1:
        return count

    array_left  = array[:len(array)/2]
    array_right = array[len(array)/2:]

    for i in range (0, len(array_left)):
        for j in range (0, len(array_right)):
            if array_left[i] > array_right[j]:
                count += 1

    count += div_and_conq(array_left)
    count += div_and_conq(array_right)
    return count



def divide_array(array):
    n = len(array)
    if n > 1:
        left = divide_array(array[0:n/2])
        right = divide_array(array[n/2:])
        return merge_and_count(left,right)
    else:
        return array


def merge_and_count(A, B):
    global merge_count
    C = []
    size_A = len(A)
    size_B = len(B)
    i, j = 0, 0
    
    while i < size_A and j < size_B:
        if A[i] <= B[j]:
            C.append(A[i])
            i = i+1
        else:
            merge_count = merge_count + len(A)-i 
            C.append(B[j])
            j = j+1
    if i == size_A: 
        C.extend(B[j:])
    else:
        C.extend(A[i:])
    return C 


def get_random_array_of_size(size):
    #returns an array of integers size 'size' 
    #integers will be within range 1-size   
    return [random.randint(1, size) for i in range(0, size)]

                     
def main():
    array = get_random_array_of_size(10)
    
    print brute_force(array)
    divide_array(array) #sorts array and puts the number of inversions in merge_count
    print merge_count
    print div_and_conq(array)


if __name__ == '__main__':
    main()
