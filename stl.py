import struct 
import copy

import numpy as np



ASCII_FACET = """  facet normal  {face[0]:e}  {face[1]:e}  {face[2]:e}
    outer loop
      vertex    {face[3]:e}  {face[4]:e}  {face[5]:e}
      vertex    {face[6]:e}  {face[7]:e}  {face[8]:e}
      vertex    {face[9]:e}  {face[10]:e}  {face[11]:e}
    endloop
  endfacet"""

BINARY_HEADER ="80sI"
BINARY_FACET = "12fH"      


def parse_ascii_stl(f): 
    """expects a filelike object, and returns a nx12 array. One row for every facet in the STL file."""
    
    stack = []
    facets = []
    line = f.readline()
    while line: 
        

        if "facet normal" in line: 

            stack.extend(map(float,line.strip().split()[2:5]))
            line = f.readline() #"outer loop"
            #vertecies
            line = f.readline() 
            stack.extend(map(float,line.strip().split()[1:4]))
            line = f.readline() 
            stack.extend(map(float,line.strip().split()[1:4]))
            line = f.readline() 
            stack.extend(map(float,line.strip().split()[1:4]))
            line = f.readline() #"end loop"
            line = f.readline() #'endfacet'

            facets.append(stack)
            stack = []

        line = f.readline()

    return np.array(facets)

def parse_binary_stl(f): 

    header,n_triangles = struct.unpack(BINARY_HEADER,f.read(84))

    facets = []
    
    for i in xrange(0,n_triangles):
        facet = struct.unpack(BINARY_FACET,f.read(50))
        facets.append(facet[:12])

    return np.array(facets)    


class STL(object): 
    """Manages the points extracted from an STL file""" 

    def __init__(self,stl_file): 
        """given an stl file object, imports points and reshapes array to an 
        array of n_facetsx3 points.""" 

        if not hasattr(stl_file,'readline'): 
            stl_file = open(stl_file,'rb')

        ascii = (stl_file.readline().strip().split()[0] == 'solid')
        stl_file.seek(0)

        if ascii: 
            self.facets = parse_ascii_stl(stl_file)
        else: 
            self.facets = parse_binary_stl(stl_file)    
               
        #list of points and the associated index from the facet array 
        points = []
        stl_indecies = [] 
        point_indecies = [] #same size as stl_indecies, but points to locations in the points data

        #stl files have duplicate points, which we don't want to compute on
        #so instead we keep a mapping between duplicates and their index in 
        #the point array
        point_locations = {}
        triangles = [] #used to track connectivity information

        #extract the 9 points from each facet into one 3*n_facets set of (x,y,z)
        #    points and keep track of the original indcies at the same time so 
        #    I can reconstruct the stl file later
        column = np.arange(3,12,dtype=np.int)
        row_base = np.ones(9,dtype=np.int)

        p_count = 0 #I'm using this to avoid calling len(points) a lot
        for i,facet in enumerate(self.facets):
            row = row_base*i
            ps = facet[3:].reshape((3,3))
            triangle = []
            for p in ps: 
                t_p = tuple(p)
                try: 
                    p_index = point_locations[t_p]
                    point_indecies.append(p_index) #we already have that point, so just point back to it
                    triangle.append(p_index)
                except KeyError: 
                    points.append(p)
                    point_locations[t_p] = p_count
                    point_indecies.append(p_count)
                    triangle.append(p_count)
                    p_count += 1 
            triangles.append(tuple(triangle))

            index = np.vstack((row_base*i,column)).T.reshape((3,3,2))
            stl_indecies.extend(index)

        self.p_count = p_count
        self.stl_indecies = np.array(stl_indecies)
        #just need to re-shape these for the assignment call later
        self.stl_i0 = self.stl_indecies[:,:,0] #facet index from original stl
        self.stl_i1 = self.stl_indecies[:,:,1] #index into facet
        self.points = np.array(points)
        self.point_indecies = point_indecies
        self.triangles = np.array(triangles)

    def copy(self): 
        return copy.deepcopy(self)

    def update_points(self,points): 
        """updates the points in the object with the new set"""   

        if points.shape != self.points.shape:
            raise IndexError("The provided points set has a different shape than the original. They must be the same")

        #set the deformed points back into the original array 
        self.points = points 
        return points

    def _build_ascii_stl(self): 
        """returns a list of ascii lines for the stl file """

        lines = ['solid ffd_geom',]
        for facet in self.facets: 
            lines.append(ASCII_FACET.format(face=facet))
        lines.append('endsolid ffd_geom')
        return lines

    def _build_binary_stl(self):
        """returns a string of binary binary data for the stl file"""

        lines = [struct.pack(BINARY_HEADER,b'Binary STL Writer',len(self.facets)),]
        for facet in self.facets: 
            facet = list(facet)
            facet.append(0) #need to pad the end with a unsigned short byte
            lines.append(struct.pack(BINARY_FACET,*facet))  
        return lines      

    def get_facets(self): 
        """returns a n,3 array of facets with the x,y,z coordinates of each vertex""" 
        self.facets[self.stl_i0,self.stl_i1] = self.points[self.point_indecies]
        return self.facets


    def writeFEPOINT(self,file_name,points=None,derivs=None):
        """writes out a new FEPOINT file with the given name, using the supplied points.
        derivs is of size (3,len(points),len(control_points)), giving matricies of 
        X,Y,Z drivatives

        jacobian should have a shape of (len(points),len(control_points))"""
       
        if points != None: 
            points = self.update_points(points)
        else: 
            points = self.points    

        n_points = len(points)
        n_triangles = len(self.triangles)    

        lines = ['TITLE = "FFD_geom"',]
        var_line = 'VARIABLES = "X" "Y" "Z" "ID" '
        if derivs != None:
            n_controls = len(derivs[0][0,:])

            if len(derivs[0]) != n_points: 
                raise RuntimeError('jacobian must be of length %d, but was %d'%(n_points,len(derivs[0])))

            deriv_names = " ".join(('"XD%d" "YD%d" "ZD%d"'%(i,i,i) for i in xrange(0,n_controls))) #x,y,z derivs for reach control point
            var_line += deriv_names

        lines.append(var_line)


        lines.append('ZONE T = group0, I = %d, J = %d, F=FEPOINT'%(n_points,n_triangles)) #TODO I think this J number depends on the number of variables
        for i,p in enumerate(self.points): 
            #TODO, also have to deal with derivatives here
            #Note: point counts are 1 bias, so I have to account for that with i
            line = "%.8f %.8f %.8f %d "%(p[0],p[1],p[2],i+1) 

            if derivs != None: 
                X = np.array(derivs[0][i,:])
                Y = np.array(derivs[1][i,:])
                Z = np.array(derivs[2][i,:])
                
                line += " ".join(('%.8f %.8f %.8f'%(x,y,z) for x,y,z in zip(X,Y,Z)))

            lines.append(line)

        for tri in self.triangles: 
            line = "%d %d %d %d"%(tri[0],tri[1],tri[2],tri[2])
            lines.append(line)


        f = open(file_name,'w')
        f.write("\n".join(lines))
        f.close()


