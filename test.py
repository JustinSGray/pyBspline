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

n_X = 7000
X = linspace(0,10,n_X)

def g(X):
    """quadratic function to generate a nozzle plug"""
    X = 10-X
    return X**2+2*X+5
    
Y = g(X)



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
U = linspace(0,1,200) #parametric space



#apply the scaling to the points
#move the control points
C_y += array([0,0,4,0])
C_x += array([0,0,0,4])
C = array(zip(C_x,C_y))
X_bar = bs.calc(C)

points = bs(U)
map_points = bs(X_map)

pylab.subplot(2,1,1)
pylab.plot(points[:,0],points[:,1],c='b',label="b-spline")
pylab.scatter(map_points[:,0],map_points[:,1],c='b',label='U mapping points')
pylab.scatter(C_x,C_y,c="r",label="control points",s=50) 
pylab.axis([-2,16,0,10])
pylab.legend(loc=2)

pylab.subplot(2,1,2)
pylab.scatter(X,Y,c='g',label="orig. geom")
pylab.scatter(X_bar[:,0],Y*X_bar[:,1],c='g',marker="^",label="ffd geom") 
pylab.axis([-2,16,0,200])

pylab.legend()
pylab.show()