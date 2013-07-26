import numpy as np

import time 

from ffd_arbitrary import Shell
from stl import STL
from geometry import Geometry


start_time = time.time()

icowl = STL('test_stl/InnerCowl.stl')
ocowl = STL('test_stl/OuterCowl.stl')

print "STL Load Time: ", time.time()-start_time
start_time = time.time()


#set up centerline control points 
#NOTE: first control point is fixed in x,r
X = icowl.points[:,0]
x_max = np.max(X)
x_min = np.min(X)
n_C = 3 #control points
C_x = np.linspace(x_min,x_max,n_C) 
C_r = np.zeros((n_C,))
C_centerline = np.array(zip(C_x,C_r))


#set up thickness control points 
#NOTE: all control points fixed in x 
#NOTE: first and last control point fixed in r
n_C = 3 #number  control points
C_x = np.linspace(x_min,x_max,n_C) 
C_r = np.zeros((n_C,))
C_thickness = np.array(zip(C_x,C_r))

#body = Body(centerbody,n_C=10) #just makes n_C evenly spaced points
shell = Shell(ocowl, icowl, C_centerline, C_thickness, name="cowl") #uses given tuples of points
shell0 = shell.copy()

geom = Geometry()
geom.add(shell0,name="c0")
geom.add(shell,name="cowl")

#params = geom.get_params() #params['centerbody'] = [(0,0),]

print "Bspline Compute Time: ", time.time()-start_time
start_time = time.time()

#calculate new P's

deltaC_x = [0,0,0]
deltaC_r = [0,0,0]
deltaC_c = np.array(zip(deltaC_x,deltaC_r))

deltaC_x = [0,0,0]
deltaC_r = [0,1,0]
deltaC_t = np.array(zip(deltaC_x,deltaC_r))

geom.deform(cowl=(deltaC_c, deltaC_t))


print "Run Time: ", time.time()-start_time
    
geom.writeSTL('new.stl', ascii=False)
geom.writeFEPOINT('deform.dat')

#geometry.writeSTL('new.stl',body.coords.cartesian,ascii=False)
#centerbody.writeFEPOINT('deform.dat',body.coords.cartesian)








