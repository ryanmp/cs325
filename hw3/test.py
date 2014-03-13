import time, sys, cPickle


d = {}

big = 15000*15000/2
print big
test_size = int(1e7)
print test_size

start_time = time.time()
for i in xrange(int(test_size)):
	d[i] = (i,'ok')
print time.time() - start_time

print "size in mem:", sys.getsizeof(d)

#d_serial = cPickle.dumps(d)
#print "size as string:", sys.getsizeof(d_serial)
