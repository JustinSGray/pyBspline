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

centerbody = Body(centerbody,controls=5,name="centerbody")
cowl = Shell(outer_cowl,inner_cowl,5,5,name="cowl")
shroud = Shell(outer_shroud,inner_shroud,5,5,name="shroud")

geom = Geometry()
geom.add(centerbody)
geom.add(cowl)
geom.add(shroud)

print "Geom Calc Time: ", time.time()-start_time
start_time = time.time()
