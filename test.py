from numpy.random import random_sample
from numpy import linspace, array

from matplotlib import pylab

from bspline import Bspline

C = array([[0.08,0.08],
           #[0,0],
           [.1,.5],
           [.7,.7],
           [.8,1.2],
           [1.4,1.4],
           [1.5,1.5]
           ])
           
C = random_sample((10,2))

pylab.scatter(*zip(*C),c='r',marker='o')

bs = Bspline(C,4)
X = linspace(0,1,500)
pylab.plot(*zip(*bs(X)))

pylab.show()
    


