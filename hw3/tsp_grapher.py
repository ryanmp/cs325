import matplotlib.pyplot as plt
import numpy as np


def plot_cities(cities):
	x_val = [x[0] for x in cities]
	y_val = [x[1] for x in cities]
	plt.scatter(x_val,y_val)
	plt.show()

def plot_route(cities, route):
	X, Y = [],[]
	for i in route:
		X.append([cities[i][0]])
		Y.append([cities[i][1]])

	X.append([cities[route[0]][0]])
	Y.append([cities[route[0]][1]])    

	plt.plot(X, Y, 'bo-')


	'''
	for i in xrange(len(route)):
		plt.annotate(route[i],  xy = (X[i][0], Y[i][0]), xytext = (-20, -20),
	        textcoords = 'offset points', ha = 'right', va = 'bottom',
	        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
	        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
	'''
	


	plt.show()
	
def plot_routes(cities, routes):

	styles = ['ro-','go:','bo--','co-.']
	widths = [1.0,3.0,2.0]

	for idx, route in enumerate(routes):
		X, Y = [],[]
		for i in route:
			X.append([cities[i][0]])
			Y.append([cities[i][1]])

		X.append([cities[route[0]][0]])
		Y.append([cities[route[0]][1]])    
		plt.plot(X, Y, styles[idx], linewidth=widths[idx])

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

	plt.xlim([_ranges[0][0],_ranges[0][-1]])

	plt.show()
	return slopes, intercepts

def plot_improvements(_ls, _ts, n):
	for i in xrange(len(_ls)):
		plt.plot(_ls[i],_ts[i],label=str(n)+" cities")
	plt.legend(loc='upper left')
	plt.ylabel('route length')
	plt.xlabel('iterations')
	plt.show()
	

def plot_lengths(_ls, _ranges, algos):
	for i in xrange(len(_ls)):
		plt.plot(_ranges[i],_ls[i],label=algos[i].__name__)
	plt.legend(loc='upper left')
	plt.xlabel('n')
	plt.ylabel('route length')
	plt.show()