import numpy as np

import time 

from ffd import Body, Shell
from stl import STL
from geometry import Geometry


start_time = time.time()

centerbody = STL('NozzleSurfacesBin/Centerbody_Bin.stl')
inner_cowl = STL('NozzleSurfacesBin/InnerCowl_Bin.stl')
outer_cowl = STL('NozzleSurfacesBin/OuterCowl_Bin.stl')
inner_shroud = STL('NozzleSurfacesBin/InnerShroud_Bin.stl')
outer_shroud = STL('NozzleSurfacesBin/OuterShroud_Bin.stl')

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

centerbody = Body(centerbody, controls=n_C, r_ref=100, x_ref=1000)
cowl = Shell(outer_cowl, inner_cowl, n_C, n_C, r_ref=100, x_ref=1000)
shroud = Shell(outer_shroud, inner_shroud, n_C, n_C, r_ref=100, x_ref=1000)

geom = Geometry()
geom.add(centerbody, name="centerbody")
geom.add(cowl, name="cowl")
geom.add(shroud, name="shroud")

print "Geom Calc Time: ", time.time()-start_time
start_time = time.time()

deltaC_x = np.zeros((n_C,))
deltaC_x[3:] = 1
deltaC_r = np.zeros((n_C,))
deltaC_r[3] = 1 #second to last element, set to 10
deltaC = np.array(zip(deltaC_x,deltaC_r))
geom.deform(centerbody=deltaC)


deltaC_cx = np.zeros((n_C,))
deltaC_cr = np.zeros((n_C,))
deltaC_cx[2:] = 1 #second to last element, set to 10
deltaC_c = np.array(zip(deltaC_cx,deltaC_cr))
deltaC_tx = np.zeros((n_C,))
deltaC_tr = np.zeros((n_C,))
deltaC_t = np.array(zip(deltaC_tx,deltaC_tr))
geom.deform(cowl=(deltaC_c,deltaC_t))


import pylab as p
profile = geom.project_profile()
for point_set in profile: 
    X = point_set[:,0]
    Y = point_set[:,1]
    p.plot(X,Y)

p.show()