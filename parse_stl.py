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

if __name__ == '__main__':

    facet_file = open('Nozzle/Centerbody.stl','rU')

    
    print np.reshape(parse_stl(facet_file),(-1,1)).shape


class STL(object): 
    """Manages the points extracted from an STL file""" 

    def __init__(self,stl_file): 
        """given an stl file object, imports points and reshapes array to an 
        array of n_facetsx3 points.""" 

        self.facets = parse_stl(stl_file)
               
        #list of points and the associated index from the facet array 
        points = []
        indecies = [] 

        #extract the 9 points from each facet into one 3*n_facets set of (x,y,z)
        #    points and keep track of the original indcies at the same time so 
        #    I can reconstruct the stl file later
        column = range(3,12)
        for i,facet in enumerate(self.facets):
            row = 9*[i,]
            
            indecies.extend(np.array(zip(row,column)).reshape((3,3,2)))
            points.extend(facet[3:].reshape((3,3)))

        self.indecies = np.array(indecies)
        #just need to re-shape these for the assignment call later
        self.i0 = self.indecies[:,:,0]
        self.i1 = self.indecies[:,:,1]
        self.points = np.array(points)

    def write(self,file_name,points):
        """writes out a new stl file, with the given name, using the supplied 
        updated points""" 

        if points.shape != self.points.shape:
            #raise IndexError here, has to be same
            pass

        #set the deformed points back into the original array 
        self.points = points.copy()
        self.facets[self.i0,self.i1] = points

        lines = ['solid ffd_geom',]
        for facet in self.facets: 
            lines.append(ASCII_FACET.format(face=facet))
        lines.append('endsolid ffd_geom')    

        f = open(file_name,'w')
        f.write("\n".join(lines))
        f.close()


