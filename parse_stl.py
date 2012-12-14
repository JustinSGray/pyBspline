from pyparsing import Word,Literal,CaselessLiteral,Combine,Optional,nums,ParseException

import numpy as np

ASCII_FACET = """  facet normal  {face[0]:e}  {face[1]:e}  {face[2]:e}
    outer loop
      vertex    {face[3]:e}  {face[4]:e}  {face[5]:e}
      vertex    {face[6]:e}  {face[7]:e}  {face[8]:e}
      vertex    {face[9]:e}  {face[10]:e}  {face[11]:e}
    endloop
  endfacet"""




point = Literal( "." )
number = Word( "+-"+nums, nums )
ows = Optional(Word(" "))
e = CaselessLiteral("e")
#number that supports scientific notation
f_number = Combine( ows + number^(number+point) + 
               Optional(number)+
               Optional( point + Optional( Word( nums ) ) ) +
               Optional( Optional(number) + e + number )
            )


facet = ows + Literal('facet')
facet_end   = ows + Literal('endfacet')
normal      = ows + Literal('normal')
loop_start  = ows + Literal('outer loop')
loop_end    = ows + Literal('endloop')

facet_normal = facet + normal + f_number + f_number + f_number
vertex = ows + Literal('vertex') + f_number + f_number + f_number

def _parse(str): 
    for t in [facet_normal,vertex,loop_start,loop_end,facet_end]:
        try: 
            tokens = t.parseString(str)
            return t, tokens
        except ParseException: 
            pass
    return False,False    

def parse_stl(f): 
    """expects a filelike object, and returns a nx12 array. One row for every facet in the STL file."""
    
    if not hasattr(f,'readline'): 
        f = open(f,'rb')

    line = f.readline()
    stack = []
    facets = []
    while line: 
        #print "parsing line:", line.strip()
        #print "    stack: ", len(stack)
        t,tokens = _parse(line)
        if t==facet_normal: 
            stack = []
            stack.extend([float(x) for x in tokens[2:5]])
        
        elif t==vertex: 
            stack.extend([float(x) for x in tokens[1:4]])
        
        elif t==facet_end: 
            #empty the stack into the growing array of points
            facets.append(stack)
            pass

        line = f.readline()

    return np.array(facets)


class STL(object): 
    """Manages the points extracted from an STL file""" 

    def __init__(self,stl_file): 
        """given an stl file object, imports points and reshapes array to an 
        array of n_facetsx3 points.""" 

        self.facets = parse_stl(stl_file)
               
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

        p_count = 0
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
                    p_count += 1 
            triangles.append(tuple(triangle))

            index = np.vstack((row_base*i,column)).T.reshape((3,3,2))
            stl_indecies.extend(index)

        self.stl_indecies = np.array(stl_indecies)
        #just need to re-shape these for the assignment call later
        self.stl_i0 = self.stl_indecies[:,:,0]
        self.stl_i1 = self.stl_indecies[:,:,1]
        self.points = np.array(points)
        self.point_indecies = point_indecies
        self.triangles = triangles

    def update_points(self,points): 
        """updates the points in the object with the new set"""   

        if points.shape != self.points.shape:
            #raise IndexError here, has to be same
            pass

        #set the deformed points back into the original array 
        self.points = points 
        return points

    def writeSTL(self,file_name,points=None):
        """writes out a new stl file, with the given name, using the supplied 
        updated points""" 

        if points: 
            points = self.update_points(points)
        
        self.facets[self.stl_i0,self.stl_i1] = points[self.point_indecies]

        lines = ['solid ffd_geom',]
        for facet in self.facets: 
            lines.append(ASCII_FACET.format(face=facet))
        lines.append('endsolid ffd_geom')    

        f = open(file_name,'w')
        f.write("\n".join(lines))
        f.close()

    def exportFEPOINT(self,file_name,points=None):
       """writes out a new FEPOINT file with the given name, using the supplied points"""
       
       if points: 
            points = self.update_points(points)

       pass          

    def exportRAW(self,file_name,points=None): 
        """writes out a simple comma separated datafile that can be parsed 
        a lot faster""" 

        if points: 
            points = self.update_points(points)

        pass

