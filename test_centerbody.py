import numpy as np


from ffd_arbitrary import Body
from parse_stl import parse_stl

facets = parse_stl(open('nozzle/Centerbody_test.stl','rb'))

#list of points and the associated index from the facet array 
points = []
indecies = [] 

#extract the 9 points from each facet into one 3*n_facets set of (x,y,z)
#    points and keep track of the original indcies at the same time so 
#    I can reconstruct the stl file later
column = range(3,12)
for i,facet in enumerate(facets):
    row = 9*[i,]
    
    indecies.extend(np.array(zip(row,column)).reshape((3,3,2)))
    points.extend(facet[3:].reshape((3,3)))

indecies = np.array(indecies)
points = np.array(points)

#set up control points 
X = points[:,0]
x_max = np.max(X)
x_min = np.min(X)
n_C = 10 #10 control points
C_x = np.linspace(x_min,x_max,n_C) 
C_r = np.zeros((n_C,))
C = np.array(zip(C_x,C_r))


#set the deformed points back into the original array 
new_facets = facets.copy()
new_facets[indecies[:,:,0],indecies[:,:,1]] = points

#write out a new stl file


ASCII_FACET = """facet normal  {face[0]:e}  {face[1]:e}  {face[2]:e}
    outer loop
      vertex    {face[3]:e}  {face[4]:e}  {face[5]:e}
      vertex    {face[6]:e}  {face[7]:e}  {face[8]:e}
      vertex    {face[9]:e}  {face[10]:e}  {face[11]:e}
    endloop
    endfacet"""

lines = ['solid ffd_geom',]
for facet in new_facets: 
    lines.append(ASCII_FACET.format(face=facet))
lines.append('endsolid ffd_geom')

f = open('new.stl','w')
f.write("\n".join(lines))
f.close()




