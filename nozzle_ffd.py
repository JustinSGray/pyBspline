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
