import numpy as np


from ffd_arbitrary import Body
from parse_stl import STL
import time 

start_time = time.time()


#centerbody= STL('nozzle/Centerbody.stl')
centerbody= STL('NozzleSurfacesBin/Centerbody_Bin.stl')

points = centerbody.points

#set up control points 
X = points[:,0]
x_max = np.max(X)
x_min = np.min(X)
n_C = 10 #10 control points
C_x = np.linspace(x_min,x_max,n_C) 
C_r = np.zeros((n_C,))
C = np.array(zip(C_x,C_r))

body = Body(points,C)

deltaC_x = [0,0,0,0,0,0,0,0,0,0]
deltaC_r = [0,0,0,0,0,0,0,0,10,0]
deltaC = np.array(zip(deltaC_x,deltaC_r))

print "Load Time: ", time.time()-start_time
start_time = time.time()



#calculate new P's
N = 50
for i in xrange(N): 
    deltaC_x = [0,0,0,0,0,0,0,0,0,0]
    deltaC_r = [0,0,0,0,0,0,0,0,i,0]
    deltaC = np.array(zip(deltaC_x,deltaC_r))
    body.deform(deltaC)

print "Run Time: ", (time.time()-start_time)/float(N)
    
centerbody.writeSTL('new.stl',body.coords.cartesian,ascii=False)
#centerbody.writeFEPOINT('deform.dat',body.coords.cartesian)








