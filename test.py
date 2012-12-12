from matplotlib import pylab

from numpy.random import random_sample
from numpy import linspace, array, zeros, ones

from ffd_revolve import Body
import time

#test points
n_X = 10
X = linspace(0,10,n_X)

def g(X):
    """quadratic function to generate a nozzle plug"""
    X = 10-X
    return X**2+2*X+5
    
R = g(X)
P = array(zip(X,R))


#generate some control points
n_C = 4
C_x = linspace(0,10,n_C)
C_r = zeros(n_C)
C = array(zip(C_x,C_r))

body = Body(P,C)

#apply the scaling to the points
#move the control points
deltaC_r = array([0,0,1,0])
deltaC_x = array([0,0,0,0])
deltaC = array(zip(deltaC_x,deltaC_r))
body.deform(deltaC)

fig = pylab.figure()
ax = fig.add_subplot(2,1,1)
body.plot_spline(ax)
ax.legend(loc=2)

ax = fig.add_subplot(2,1,2)
body.plot_geom(ax)

pylab.legend()
pylab.show()