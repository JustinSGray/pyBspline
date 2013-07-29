import numpy as np

import time 

from ffd import Body
from stl import STL
from geometry import Geometry


start_time = time.time()


#centerbody= STL('nozzle/Centerbody.stl')
centerbody= STL('NozzleSurfacesBin/Centerbody_Bin.stl')

print "STL Load Time: ", time.time()-start_time
start_time = time.time()


n_c = 3
body = Body(centerbody,controls=n_c) #just makes n_C evenly spaced points
#body = Body(centerbody,C,name="centerbody") #uses given tuples of points
body0 = body.copy()

geom = Geometry()
geom.add(body0,name="cb0")
geom.add(body,name="centerbody")

#params = geom.get_params() #params['centerbody'] = [(0,0),]

print "Bspline Compute Time: ", time.time()-start_time
start_time = time.time()

deltaC_x = np.zeros((n_c,))
deltaC_r = np.zeros((n_c,))
deltaC_r[-2] = 10 #second to last element, set to 10
deltaC = np.array(zip(deltaC_x,deltaC_r))

geom.deform(centerbody=deltaC)

print "Run Time: ", time.time()-start_time
start_time = time.time()
    
geom.writeSTL('new.stl', ascii=False)

print "STL Write Time: ", time.time()-start_time
start_time = time.time()

geom.writeFEPOINT('deform.dat')

print "FEPoint Write Time: ", time.time()-start_time


#geometry.writeSTL('new.stl',body.coords.cartesian,ascii=False)
#centerbody.writeFEPOINT('deform.dat',body.coords.cartesian)









