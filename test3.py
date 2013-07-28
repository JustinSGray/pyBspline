import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D

from ffd import Body


#Baseline geometry
X = np.linspace(0,10,10)
Ro = 300*np.ones((10,))

n_theta = 20
Theta = np.linspace(0,2*np.pi,n_theta)
ones = np.ones(len(X))
sin_theta = np.sin(Theta)
cos_theta = np.cos(Theta)

P = []
for t in Theta: 
    P.extend(zip(X,Ro,t*ones))
P = np.array(P)    

#center line control points
n_Cc = 4
Cc_x = np.linspace(0,10,n_Cc)
Cc_r = np.zeros((n_Cc,))
Cc = np.array(zip(Cc_x,Cc_r))


body = Body(P,Cc,cartesian=False)

#move the control points for centerline
deltaC_r = np.array([0,2,0,0])
deltaC_x = np.array([0,0,0,1])
deltaCc = np.array(zip(deltaC_x,deltaC_r))

#calculate new P's
body.deform(deltaCc)

fig = pylab.figure()
ax = fig.add_subplot(3,1,1)
ax.set_title('Centerline b-sPiine Interpolant')
body.plot_spline(ax)
ax.legend(loc=2)


ax = fig.add_subplot(3,1,3)
ax.set_title('Initial and Final Geometries')
body.plot_geom(ax)

ax.legend()


fig = pylab.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(body.Xo,body.Yo,body.Zo,rstride=1, cstride=1, alpha=0.2)
#ax.plot_surface(body.Xi,body.Yi,body.Zi,rstride=1, cstride=1, alpha=1.0,color='r')
       
pylab.show()