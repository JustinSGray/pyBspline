from numpy.random import random_sample
from numpy import linspace, array

from matplotlib import pylab

from bspline import Bspline

import time
import timeit

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
X = linspace(0,1,5000)

t0 = time.time()

pylab.plot(*zip(*bs(X)))

timer = timeit.Timer("bs(X)")
print "%.2f usec/pass" % (1000000 * t.timeit(number=100000)/100000)


pylab.show()
    


