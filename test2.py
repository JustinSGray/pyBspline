import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D

from ffd_arbitrary import Shell


#Baseline geometry
X = np.linspace(0,10,10)
Ro = 300*np.ones((10,))
Ri = Ro.copy()
Ri[1:-1] *= .5

P_outter = np.array(zip(X,Ro))
P_inner = np.array(zip(X,Ri))
P = np.vstack((P_outter,P_inner))

#center line control points
n_Cc = 4
Cc_x = np.linspace(0,10,n_Cc)
Cc_r = np.zeros((n_Cc,))
Cc = np.array(zip(Cc_x,Cc_r))

#thickness control points
n_Ct = 4
Ct_x = np.linspace(0,10,n_Ct)
Ct_r = np.zeros((n_Ct,))
Ct = np.array(zip(Ct_x,Ct_r))

shell = Shell(P_outter,P_inner,Cc,Ct)

#move the control points for centerline
deltaC_r = np.array([0,2,0,0])
deltaC_x = np.array([0,0,0,1])
deltaCc = np.array(zip(deltaC_x,deltaC_r))

#move the control points for thickness (only in r direction)
deltaC_r = np.array([0,-.15,.1,0])
deltaC_x = np.array([0,0,0,0])
deltaCt = np.array(zip(deltaC_x,deltaC_r))

#calculate new P's
shell.deform(deltaCc,deltaCt)

fig = pylab.figure()
ax = fig.add_subplot(3,1,1)
ax.set_title('Centerline b-sPiine Interpolant')
shell.plot_centerline_spline(ax)
ax.legend(loc=2)

ax = fig.add_subplot(3,1,2)
ax.set_title('Thickness b-sPiine Interpolant')
shell.plot_thickness_spline(ax)
ax.legend(loc=2)

ax = fig.add_subplot(3,1,3)
ax.set_title('Initial and Final Geometries')
shell.plot_geom(ax)

ax.legend()


fig = pylab.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(shell.Xo,shell.Yo,shell.Zo,rstride=1, cstride=1, alpha=0.2)
ax.plot_surface(shell.Xi,shell.Yi,shell.Zi,rstride=1, cstride=1, alpha=1.0,color='r')
       
pylab.show()