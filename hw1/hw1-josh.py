#Joshua Villwock
#CS325: Analysis of Algotithms
#1/25/2014
#Implmentation Assignment 1

import random
import timeit
#1.  Brute-force:
# O(n^2)
#for (1 ... n)
#    compare i with i+1 through n
#        if i is larger, increment
def brutecount(lst):
    print "Brute Count:"
    i = 0
    count = 0
    L = len(lst)
    while i < L:
        for n in lst[i+1:]:  #The [i+1:] is python notation for chopping off parts of lists
            if n < lst[i]:
                count += 1
        i += 1
    print count

#2.  Naive Divide and Conquer
#Should be close to O n*Log(n)
#dividecount is the master function, dividecounthelper does the appending
def dividecounthelper(a, b):
    assert a == sorted(a) and b == sorted(b)  #Make sure both lists are sorted.
    c = []
    count = 0
    i, j = 0, 0
    while i < len(a) and j < len(b):
        c.append(min(b[j], a[i]))
        if b[j] < a[i]:
            count += len(a) - i
            j+=1
        else:
            i+=1
    # now we reached the end of one the lists
    c += a[i:] + b[j:] # append the remainder of the list
    return count, c
#I just realized this may not be exactly what you were shooting for the divide and conquer, and
#May be pushing it, but it's too late now, and it is technically divide and conquer.
def dividecount(L):
    if len(L) == 1: return 0, L
    n = len(L) // 2
    a, b = L[:n], L[n:]
    ra, a = dividecount(a)
    rb, b = dividecount(b)
    r, L = dividecounthelper(a, b)
    return ra+rb+r, L
#This function just prints and sets stuff for us, which then calls the real functions, above.
def dividecountrun(L):
    print "Divide Count:"
    print dividecount(L)[0]

#3.  Merge and count.
#Basically runs a mergesort, but counts everytime elements are out of order
#This results in us being able to count inversions in O(n log n) time
#I'm using 3 functions for this for ease of use:

#Just a wrapper for the mergesort & merge functions.
def mergecountold(lst):
    global count
    count = 0
    print "Merge Count:"
    mergesort(lst)
    print count
    count = 0

#Handles the merging and counting
def merge(left, right):
    global count
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            count += len(left) - i
    result += left[i:]
    result += right[j:]
    return result

#Handles the splitting and checking
def mergesort(lst):
    if len(lst) <= 1:
        return lst
    middle = int( len(lst) / 2 )
    left = mergesort(lst[:middle])
    right = mergesort(lst[middle:])
    return merge(left, right)

#Alternate Merge Sort Functions:
#Should work the same, just better, but seems to be messed up :/
#Basically runs a mergesort, but counts everytime elements are out of order
#This results in us being able to count inversions in O(n log n) time
def mergecount2(lst):
    global count
    count = 0
    print "Merge Count 2:"
    print mergesort2(lst)
    print count
    count = 0

def merge2(left, right):
    global count
    C = []
    lenLeft=len(left)
    lenRight=len(right)
    i, j = 0, 0
    while i < lenLeft and j < lenRight:
        if left[i] <= right[j]:
            C.append(left[i])
            i += 1
        else:
            #Count all the ones out of place
            count += lenLeft - i
            j += 1
    if i == lenLeft: #left get to the end
        C.extend(right[j:])
    else:
        C.extend(left[i:])
    return C
    
def mergesort2(lst):
    lenght = len(lst)   #Misspelled on purpose! Do not fix!
    if lenght > 1:
        S1 = mergesort2(lst[0:lenght/2])
        S2 = mergesort2(lst[lenght/2:])
        return merge2(S1, S2)
    else:
        return lst

#Just verifies all the algo's by running known lists through them.
def verifycorrectness():
    #------------------Edit This to verify with custom lists------------------------#
    listToCount = [2, 3, 1, 4, 5, 6, 8, 7, 9, 10, 11, 12]
    #------------------Edit This to verify with custom lists------------------------#
    brutecount(listToCount)
    dividecountrun(listToCount)
    mergecountold(listToCount)
    #mergecount2(listToCount)

#Generates random ints of quantity "Length" and tries every function, counting completion time.
def testrandom(Length):
    print "Generating list of ", Length, " Random Numbers..."
    listToCount = [int(1000*random.random()) for i in xrange(Length)]
    t1 = timeit.Timer(lambda: brutecount(listToCount))
    print t1.timeit(1), " Seconds"
    t2 = timeit.Timer(lambda: dividecountrun(listToCount))
    print t2.timeit(1), " Seconds"
    t3 = timeit.Timer(lambda: mergecountold(listToCount))
    print t3.timeit(1), " Seconds"

#Actually run them
if __name__ == "__main__":
    verifycorrectness()
    testrandom(1000)
    testrandom(2000)
    testrandom(3000)
    testrandom(4000)
    testrandom(5000)
    testrandom(10000)
    testrandom(20000)
    testrandom(30000)
    testrandom(40000)
    testrandom(50000)