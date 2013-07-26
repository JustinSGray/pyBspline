import numpy as np

import time 

from ffd_arbitrary import Body
from stl import STL
from geometry import Geometry


start_time = time.time()


#centerbody= STL('nozzle/Centerbody.stl')
centerbody= STL('NozzleSurfacesBin/Centerbody_Bin.stl')

print "STL Load Time: ", time.time()-start_time
start_time = time.time()


#set up control points 
X = centerbody.points[:,0]
x_max = np.max(X)
x_min = np.min(X)
n_C = 5 #10 control points
C_x = np.linspace(x_min,x_max,n_C) 
C_r = np.zeros((n_C,))
C = np.array(zip(C_x,C_r))

#body = Body(centerbody,n_C=10) #just makes n_C evenly spaced points
body = Body(centerbody,C,name="centerbody") #uses given tuples of points
body0 = body.copy()

geom = Geometry()
geom.add(body0,name="cb0")
geom.add(body,name="centerbody")

#params = geom.get_params() #params['centerbody'] = [(0,0),]

print "Bspline Compute Time: ", time.time()-start_time
start_time = time.time()

#calculate new P's

deltaC_x = [0,0,0,0,0,0,0,0,0,0]
deltaC_r = [0,0,0,0,0,0,0,0,10,0]
deltaC_x = [0,0,0,0,0]
deltaC_r = [0,0,0,10,0]
deltaC = np.array(zip(deltaC_x,deltaC_r))

geom.deform(centerbody=deltaC)

print "Run Time: ", time.time()-start_time
    
geom.writeSTL('new.stl', ascii=False)
geom.writeFEPOINT('deform.dat')

#geometry.writeSTL('new.stl',body.coords.cartesian,ascii=False)
#centerbody.writeFEPOINT('deform.dat',body.coords.cartesian)









