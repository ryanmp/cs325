import matplotlib.pyplot as plt
import numpy as np

def plot_route(cities, route):
    X, Y = [],[]
    for i in route:
        X.append([cities[i][0]])
        Y.append([cities[i][1]])

    X.append([cities[route[0]][0]])
    Y.append([cities[route[0]][1]])    

    plt.plot(X, Y, 'bo-')
    plt.show()
    

def plot_timing(_ts, _ranges, algos):
	slopes, intercepts = [], []
	for i in xrange(len(_ts)):
		plt.loglog(_ranges[i],_ts[i],basex=10,basey=10, label=algos[i].__name__)
		this_slope,this_intercept=np.polyfit(np.log(_ranges[i]),np.log(_ts[i]),1)
		slopes.append(this_slope)
		intercepts.append(this_intercept)

	plt.legend(loc='upper left')
	plt.xlabel('n')
	plt.ylabel('time (s)')
	plt.show()
	return slopes, intercepts
	

def plot_lengths(_ls, _ranges, algos):
	for i in xrange(len(_ls)):
		plt.plot(_ranges[i],_ls[i],label=algos[i].__name__)
	plt.legend(loc='upper left')
	plt.xlabel('n')
	plt.ylabel('route length')
	plt.show()