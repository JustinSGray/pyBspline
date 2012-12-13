import numpy as np


from ffd_arbitrary import Body
from parse_stl import STL

centerbody= STL('nozzle/Centerbody_test.stl')
points = centerbody.points

#set up control points 
X = points[:,0]
x_max = np.max(X)
x_min = np.min(X)
n_C = 4 #10 control points
C_x = np.linspace(x_min,x_max,n_C) 
C_r = np.zeros((n_C,))
C = np.array(zip(C_x,C_r))

body = Body(points,C)

deltaC_x = np.array([0,0,0,0])
deltaC_r = np.array([0,0,0,0])
deltaC = np.array(zip(deltaC_x,deltaC_r))

#calculate new P's
#body.deform(deltaC)

for p0,p1 in zip(points,body.coords.cartesian): 
    print p0-p1
    exit()
    

centerbody.write('new.stl',body.coords.cartesian)






