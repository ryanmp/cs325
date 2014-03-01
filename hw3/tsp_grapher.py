import matplotlib.pyplot as plt

def plot_route(cities, route):
    X, Y = [],[]
    for i in route:
        X.append([cities[i][0]])
        Y.append([cities[i][1]])

    X.append([cities[route[0]][0]])
    Y.append([cities[route[0]][1]])    

    plt.plot(X, Y, 'bo-')
    plt.show()
    
