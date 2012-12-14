import struct 
import numpy as np

from pyparsing import Word,Literal,CaselessLiteral,Combine,Optional,nums,ParseException


ASCII_FACET = """  facet normal  {face[0]:e}  {face[1]:e}  {face[2]:e}
    outer loop
      vertex    {face[3]:e}  {face[4]:e}  {face[5]:e}
      vertex    {face[6]:e}  {face[7]:e}  {face[8]:e}
      vertex    {face[9]:e}  {face[10]:e}  {face[11]:e}
    endloop
  endfacet"""

BINARY_HEADER ="80sI"
BINARY_FACET = "12fH"      




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

def parse_ascii_stl(f): 
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

def parse_binary_stl(f): 

    if not hasattr(f,'readline'): 
        f = open(f,'rb')

    header,n_triangles = struct.unpack(BINARY_HEADER,f.read(84))

    facets = []
    
    for i in xrange(0,n_triangles):
        facet = struct.unpack(BINARY_FACET,f.read(50))
        facets.append(facet[:12])

    return np.array(facets)    


class STL(object): 
    """Manages the points extracted from an STL file""" 

    def __init__(self,stl_file,ascii=True): 
        """given an stl file object, imports points and reshapes array to an 
        array of n_facetsx3 points.""" 

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

        p_count = 0 #im using this to avoid calling len(points) a lot
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

    def writeSTL(self,file_name,points=None,ascii=True):
        """writes out a new stl file, with the given name, using the supplied 
        updated points""" 

        if points != None: 
            points = self.update_points(points)
        
        self.facets[self.stl_i0,self.stl_i1] = points[self.point_indecies]

        f = open(file_name,'w')
        if ascii: 
            lines = self._build_ascii_stl()
            f.write("\n".join(lines))
        else: 
            data = self._build_binary_stl()
            f.write("".join(data))
        f.close()

    def writeFEPOINT(self,file_name,points=None):
        """writes out a new FEPOINT file with the given name, using the supplied points"""
       
        if points != None: 
            points = self.update_points(points)

        
        for tri in self.triangles: 
            print tri



