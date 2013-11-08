import time
import numpy as np

from stl import STL
from ffd_axisymmetric import Body, Shell
from geometry import Geometry


start_time = time.time()

plug = STL('NozzleSurfacesBin/Centerbody_Bin.stl')
inner_cowl = STL('NozzleSurfacesBin/InnerCowl_Bin.stl')
outer_cowl = STL('NozzleSurfacesBin/OuterCowl_Bin.stl')

print "STL Load Time: ", time.time()-start_time
start_time = time.time()


n_c = 10
body = Body(plug, controls=n_c) #just makes n_C evenly spaced points
shell = Shell(outer_cowl, inner_cowl, n_c, n_c)

print "Bspline Compute Time: ", time.time()-start_time
start_time = time.time()


geom = Geometry()
geom.add(body,name="plug")
geom.add(shell,name="cowl")

orig_points = geom.points.copy()

print "Geometry Object Building: ", time.time()-start_time
start_time = time.time()

deltaC_x = np.zeros((n_c,))
deltaC_r = np.zeros((n_c,))
#deltaC_x[-2:] = 2 
deltaC = np.array(zip(deltaC_x,deltaC_r))
geom.deform(plug=deltaC)


# deltaC_cx = np.zeros((n_c,))
# deltaC_cr = np.zeros((n_c,))
# deltaC_cr[-2] = 0 #second to last element, set to 10
# deltaC_c = np.array(zip(deltaC_cx,deltaC_cr))

# deltaC_tx = np.zeros((n_c,))
# deltaC_tr = np.zeros((n_c,))
# deltaC_tr[-2] = 0 #second to last element, set to 10
# deltaC_t = np.array(zip(deltaC_tx,deltaC_tr))
# geom.deform(cowl=(deltaC_c,deltaC_t))


print "Run Time: ", time.time()-start_time
start_time = time.time()
    
geom.writeSTL('new.stl', ascii=False)

# print "STL Write Time: ", time.time()-start_time
# start_time = time.time()

# geom.writeFEPOINT('new.fepoint')


import pylab as p
profile = geom.project_profile()
for point_set in profile: 
    X = point_set[:,0]
    Y = point_set[:,1]
    //p.scatter(X,Y)
    p.plot(X,Y)

p.show()

