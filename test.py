from matplotlib import pylab

from numpy.random import random_sample
from numpy import linspace, array, zeros, ones
from bspline import Bspline

import time

#test points
"""
C = array([[0.08,0.08],
           #[0,0],
           [.1,.5],
           [.7,.7],
           [.8,1.2],
           [1.4,1.4],
           [1.5,1.5]
           ])
           
C = random_sample((10,2))
"""
#pylab.scatter(*zip(*C),c='r',marker='o')

n_X = 50
X = linspace(0,10,n_X)

def g(X):
    """quadratic function to generate a nozzle plug"""
    X = 10-X
    return X**2+2*X+5
    
Y = g(X)
pylab.scatter(X,Y,c='g',label="base geom") 

#generate some control points
n_C = 4
C_x = linspace(0,10,n_C)
C_y = ones(n_C)
C = array(zip(C_x,C_y))

start_time = time.time()
bs = Bspline(C,X,3) #make the spline instance
print "Initial Bspline: ",time.time()-start_time

start_time = time.time()
X_map = bs.find(X) #get the mapping from parametric space to physical space
print "Points Calc: ",time.time()-start_time

#space them up to make the graph easier to read
d_y = 150

U = linspace(0,1,200) #parametric space
points = bs(U)
pylab.plot(points[:,0],points[:,1]+d_y,c='b',label="b-spline")

map_points = bs(X_map)
pylab.scatter(map_points[:,0],map_points[:,1]+d_y,c='b',label='U mapping points')
pylab.scatter(C_x,C_y+d_y,c="r",label="control points",s=50) 


#apply the scaling to the points
#move the control points
C_y += array([0,0,4,0])
C_x += array([0,0,0,4])
C = array(zip(C_x,C_y))
X_bar = bs.calc(C)
pylab.scatter(X_bar[:,0],Y*X_bar[:,1],c='g',marker="^",label="ffd geom") 

#pylab.legend(loc=3)
pylab.show()