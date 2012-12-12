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

def main(f): 
    
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
    import StringIO

    facet_str = """  facet normal  3.386098e-002  9.979581e-001  5.415772e-002
    outer loop
      vertex    3.186515e+003  2.196210e+000  0.000000e+000
      vertex    3.186260e+003  2.204885e+000  0.000000e+000
      vertex    3.186270e+003  2.191594e+000  2.385749e-001
    endloop
  endfacet"""

    facet_file = StringIO.StringIO(facet_str)

    facet_file = open('Centerbody.stl','rU')
    
    #s = "      vertex    3.186515e+003  2.196210e+000  0.000000e+000"
    #print vertex.parseString(s)

    print main(facet_file).shape



  
