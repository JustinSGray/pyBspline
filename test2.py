import numpy as np
import pylab

from ffd import Shell


#Baseline geometry
X = np.linspace(0,10,10)
Y1 = np.ones((10,))
Y2 = .5*Y1

P_upper = np.array(zip(X,Y1))
P_lower = np.array(zip(X,Y2))
P = np.vstack((P_upper,P_lower))

#center line control points
n_Cc = 4
Cc_x = np.linspace(0,10,n_Cc)
Cc_y = np.zeros((n_Cc,))
Cc = np.array(zip(Cc_x,Cc_y))

#thickness control points
n_Ct = 4
Ct_x = np.linspace(0,10,n_Ct)
Ct_y = np.zeros((n_Ct,))
Ct = np.array(zip(Ct_x,Ct_y))

shell = Shell(P_upper,P_lower,Cc,Ct)

#move the control points for centerline
deltaC_y = np.array([0,0,2,0])
deltaC_x = np.array([0,0,0,1])
deltaCc = np.array(zip(deltaC_x,deltaC_y))

#move the control points for thickness (only in y direction)
deltaC_y = np.array([0,0,0,0])
deltaC_x = np.array([0,0,0,0])
deltaCt = np.array(zip(deltaC_x,deltaC_y))

#calculate new P's
shell.deform(deltaCc,deltaCt)

pylab.subplot(3,1,1)
pylab.title('Centerline b-spline Interpolant')
pylab.scatter(Cc[:,0]+deltaCc[:,0],Cc[:,1]+deltaCc[:,1],c='red',s=50,label="Control Points")
map_points = shell.bsc_u(np.linspace(0,1,100))
pylab.plot(map_points[:,0],map_points[:,1],label="b-spline curve")
pylab.legend(loc=2)

pylab.subplot(3,1,2)
pylab.title('Thickness b-spline Interpolant')
pylab.scatter(Ct[:,0]+deltaCt[:,0],Ct[:,1]+deltaCt[:,1],c='red',s=50,label="Control Points")
map_points = shell.bst_u(np.linspace(0,1,100))
pylab.plot(map_points[:,0],map_points[:,1],label="b-spline curve")
pylab.legend(loc=2)

pylab.subplot(3,1,3)
pylab.title('Initial and Final Geometries')

pylab.scatter(shell.Pu[:,0],shell.Pu[:,1],c='g',s=50,label="initial geom")
pylab.scatter(shell.Pl[:,0],shell.Pl[:,1],c='g',s=50)
pylab.plot(shell.Pu[:,0],shell.Pu[:,1],c='g') 
pylab.plot(shell.Pl[:,0],shell.Pl[:,1],c='g') 

pylab.scatter(shell.Pu_bar[:,0],shell.Pu_bar[:,1],c='y',s=50,label="ffd geom") 
pylab.scatter(shell.Pl_bar[:,0],shell.Pl_bar[:,1],c='y',s=50) 
pylab.plot(shell.Pu_bar[:,0],shell.Pu_bar[:,1],c='y') 
pylab.plot(shell.Pl_bar[:,0],shell.Pl_bar[:,1],c='y') 

pylab.legend()


pylab.show()