from matplotlib import pylab

from numpy.random import random_sample
from numpy import linspace, array, zeros, ones

from ffd import Body
import time

#test points
n_X = 10
X = linspace(0,10,n_X)

def g(X):
    """quadratic function to generate a nozzle plug"""
    X = 10-X
    return X**2+2*X+5
    
Y = g(X)
P = array(zip(X,Y))


#generate some control points
n_C = 4
C_x = linspace(0,10,n_C)
C_y = zeros(n_C)
C = array(zip(C_x,C_y))

body = Body(P,C)

#apply the scaling to the points
#move the control points
deltaC_y = array([0,0,1,0])
deltaC_x = array([0,0,0,0])
deltaC = array(zip(deltaC_x,deltaC_y))
body.deform(deltaC)


pylab.subplot(2,1,1)
map_points = body.bs(linspace(0,1,100))
pylab.plot(map_points[:,0],map_points[:,1],c='b',label="b-spline")
pylab.scatter(body.C_bar[:,0],body.C_bar[:,1],c="r",label="control points",s=50) 
pylab.legend(loc=2)

pylab.subplot(2,1,2)
pylab.scatter(body.P[:,0],body.P[:,1],c='g',label="orig. geom")
pylab.scatter(body.P_bar[:,0],body.P_bar[:,1],c='g',marker="^",label="ffd geom") 

pylab.legend()
pylab.show()