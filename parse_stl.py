from pyparsing import Word,Literal,CaselessLiteral,Combine,Optional,nums,ParseException

import numpy as np

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

def import(f): 
    """expects a filelike object, and returns a nx12 array. One row for every facet in the STL file."""
    
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

    facet_file = open('Centerbody.stl','rU')

    
    print np.reshape(import(facet_file),(-1,1)).shape



  
