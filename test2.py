import numpy as np
import pylab
from mpl_toolkits.mplot3d import Axes3D

from ffd import Shell


#Baseline geometry
X = np.linspace(0,10,10)
Ro = 300*np.ones((10,))
Ri = .5*Ro

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
deltaC_r = np.array([-.1,-.15,.1,0])
deltaC_x = np.array([0,0,0,0])
deltaCt = np.array(zip(deltaC_x,deltaC_r))

#calculate new P's
shell.deform(deltaCc,deltaCt)

pylab.subplot(3,1,1)
pylab.title('Centerline b-sPiine Interpolant')
pylab.scatter(Cc[:,0]+deltaCc[:,0],Cc[:,1]+deltaCc[:,1],c='red',s=50,label="Control Points")
map_points = shell.bsc_o(np.linspace(0,1,100))
pylab.plot(map_points[:,0],map_points[:,1],label="b-sPiine curve")
pylab.legend(loc=2)

pylab.subplot(3,1,2)
pylab.title('Thickness b-sPiine Interpolant')
pylab.scatter(Ct[:,0]+deltaCt[:,0],Ct[:,1]+deltaCt[:,1],c='red',s=50,label="Control Points")
map_points = shell.bst_o(np.linspace(0,1,100))
pylab.plot(map_points[:,0],map_points[:,1],label="b-sPiine curve")
pylab.legend(loc=2)

pylab.subplot(3,1,3)
pylab.title('Initial and Final Geometries')

pylab.scatter(shell.Po[:,0],shell.Po[:,1],c='g',s=50,label="initial geom")
pylab.scatter(shell.Pi[:,0],shell.Pi[:,1],c='g',s=50)
pylab.plot(shell.Po[:,0],shell.Po[:,1],c='g') 
pylab.plot(shell.Pi[:,0],shell.Pi[:,1],c='g') 

pylab.scatter(shell.Po_bar[:,0],shell.Po_bar[:,1],c='y',s=50,label="ffd geom") 
pylab.scatter(shell.Pi_bar[:,0],shell.Pi_bar[:,1],c='y',s=50) 
pylab.plot(shell.Po_bar[:,0],shell.Po_bar[:,1],c='y') 
pylab.plot(shell.Pi_bar[:,0],shell.Pi_bar[:,1],c='y') 

pylab.legend()


fig = pylab.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(shell.Xo,shell.Yo,shell.Zo,rstride=1, cstride=1, alpha=0.2)
ax.plot_surface(shell.Xi,shell.Yi,shell.Zi,rstride=1, cstride=1, alpha=1.0,color='r')
       
pylab.show()