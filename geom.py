from ffd_revolve import Body,Shell
from matplotlib import pylab as plt
import numpy as np

def import_points(file): 
	X = []
	R = []
	for line in file: 
	    data = [float(c) for c in line.split()]
	    X.append(data[0])
	    R.append(data[1])    	
	return np.array(X), np.array(R) 
	file.close() 
	  

#central body 
X,R = import_points(open('baseline_geom/CenterBody.txt','rb'))
P_body = np.array(zip(X,R))

#body control points
n_C = 4
C_x = np.linspace(0,10,n_C)
C_r = np.zeros(n_C)
C_body = np.array(zip(C_x,C_r))

body = Body(P_body,C_body,name="plug")


############################
#Inner Shell
############################
Xo,Ro = import_points(open('baseline_geom/OuterShroud.txt','rb'))
Xi,Ri = import_points(open('baseline_geom/InnerShroud.txt','rb'))

P_outer = np.array(zip(Xo,Ro))
P_inner = np.array(zip(Xi,Ri))

print P_outer[-1]
print P_inner[-1]

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

shell1 = Shell(P_outer,P_inner,Cc,Ct,name='Inner Shell')


############################
#Outer Shell
############################
Xo,Ro = import_points(open('baseline_geom/OuterCowl.txt','rb'))
Xi,Ri = import_points(open('baseline_geom/InnerCowl.txt','rb'))

P_outer = np.array(zip(Xo,Ro))
P_inner = np.array(zip(Xi,Ri))

print P_outer[-1]
print P_inner[-1]

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

shell2 = Shell(P_outer,P_inner,Cc,Ct,name='Inner Shell')

#plot the undeformed geometry
fig = plt.figure()
ax = fig.gca()
body.plot_geom(ax,ffd_color=None)
shell1.plot_geom(ax,initial_color='r',ffd_color=None)
shell2.plot_geom(ax,initial_color='b',ffd_color=None)

plt.legend()
plt.show()

