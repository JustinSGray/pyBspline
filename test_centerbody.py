import numpy as np


from ffd_arbitrary import Body
from parse_stl import STL

centerbody= STL('nozzle/Centerbody_test.stl')
points = .5*centerbody.points

#set up control points 
X = points[:,0]
x_max = np.max(X)
x_min = np.min(X)
n_C = 10 #10 control points
C_x = np.linspace(x_min,x_max,n_C) 
C_r = np.zeros((n_C,))
C = np.array(zip(C_x,C_r))

centerbody.write('new.stl',points)






