import time
import numpy as np

from stl import STL
from ffd_axisymmetric import Body, Shell
from geometry import Geometry


start_time = time.time()

plug = STL('NozzleSurfacesBin/Centerbody_Bin.stl')
innerCowl = STL('NozzleSurfacesBin/InnerCowl_Bin.stl')
outerCowl = STL('NozzleSurfacesBin/OuterCowl_Bin.stl')

#plug = STL('nozzle/plug.stl')
cowl = STL('nozzle/cowl.stl')

print "STL Load Time: ", time.time()-start_time

start_time = time.time()

n_c = 10

body = Body(plug, controls=n_c) #just makes n_C evenly spaced points
#shell = Shell(cowl, cowl.copy(), n_c, n_c)
shell = Shell(outerCowl, innerCowl, n_c, n_c)

print "Bspline Compute Time: ", time.time()-start_time
start_time = time.time()


geom = Geometry()
geom.add(body, name="plug")
geom.add(shell, name="cowl")

print "Geometry Object Building: ", time.time()-start_time
start_time = time.time()


baseline = Geometry()
baseline.add(body.copy(), name="plug")
baseline.add(shell.copy(), name="cowl")

deltaC_x = np.zeros((n_c,))
deltaC_r = np.zeros((n_c,))
deltaC_x[-2] = 100 #second to last element, set to 10
deltaC_x[-2] = .025 #second to last element, set to 10
deltaC_x[-1] = -.025 #second to last element, set to 10
deltaC = np.array(zip(deltaC_x, deltaC_r))
geom.deform(plug=deltaC)
print deltaC_x
print deltaC_r

# deltaC_cx = np.zeros((n_c,))
# deltaC_cr = np.zeros((n_c,))
# deltaC_cr[:] = 2 #second to last element, set to 10
# print deltaC_cx
# print deltaC_cr
# deltaC_c = np.array(zip(deltaC_cx, deltaC_cr))
# deltaC_tx = np.zeros((n_c,))
# deltaC_tr = np.zeros((n_c,))
# deltaC_tr[-2] = .01 #second to last element, set to 10
# print deltaC_tr
# deltaC_t = np.array(zip(deltaC_tx, deltaC_tr))
# geom.deform(cowl=(deltaC_c, deltaC_t))


print "Run Time: ", time.time()-start_time
start_time = time.time()
    
# geom.writeSTL('new.stl', ascii=False)

# print "STL Write Time: ", time.time()-start_time
# start_time = time.time()

# geom.writeFEPOINT('new.fepoint')



import pylab as p
profile = geom.project_profile()
profile_base = baseline.project_profile()

for point_set in profile: 
    X = point_set[:,0]
    Y = point_set[:,1]
    p.plot(X,Y, c='b')
    
for point_set in profile_base: 
    X = point_set[:,0]
    Y = point_set[:,1]
    p.plot(X,Y, c='r')
    
    

p.show()

