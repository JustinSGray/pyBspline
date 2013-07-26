import struct

from stl import ASCII_FACET, BINARY_HEADER, BINARY_FACET

from ffd_arbitrary import Body, Shell


class Geometry(object): 

    def __init__(self): 

        self._comps = []
        self._i_comps = {}
        self._n_comps = 0 


    def _get_points_and_tris(self): 
        """returns all the points and triangle indecies in the whole geometry""" 
        
        points = []
        tris = []
        i_offset = 0
        for comp in self._comps: 
            coords = comp.coords.cartesian
            points.extend(coords)
            tris.extend()
            i_offset += len(coords)

    def add(self, comp ,name=None): 
        """ addes a new component to the geometry""" 

        if (name is None) and (comp.name is None): 
            name = "comp_%d"%self._n_comps

        self._i_comps[name] = self._n_comps
        self._comps.append(comp)
        self._n_comps += 1


    def get_parameters(self): 
        """ returns a dictionary of parameters sets key'd to component names"""
        pass

    def deform(self,**kwargs): 
        """ deforms the geometry applying the new locations for the control points, given by body name"""
        for name,delta_C in kwargs.iteritems(): 
            i = self._i_comps[name]
            comp = self._comps[i]
            if isinstance(comp,Body):
                comp.deform(delta_C)
            else:
                comp.deform(*delta_C)

    def _build_ascii_stl(self, facets): 
        """returns a list of ascii lines for the stl file """

        lines = ['solid ffd_geom',]
        for facet in facets: 
            lines.append(ASCII_FACET.format(face=facet))
        lines.append('endsolid ffd_geom')
        return lines

    def _build_binary_stl(self, facets):
        """returns a string of binary binary data for the stl file"""

        lines = [struct.pack(BINARY_HEADER,b'Binary STL Writer',len(facets)),]
        for facet in facets: 
            facet = list(facet)
            facet.append(0) #need to pad the end with a unsigned short byte
            lines.append(struct.pack(BINARY_FACET,*facet))  
        return lines      

    def writeSTL(self, file_name, ascii=False): 
        """outputs an STL file"""
        
        facets = []
        for comp in self._comps: 
            if isinstance(comp,Body): 
               facets.extend(comp.stl.get_facets())
            else: 
               facets.extend(comp.outer_stl.get_facets())
               facets.extend(comp.inner_stl.get_facets())

        f = open(file_name,'w')
        if ascii: 
            lines = self._build_ascii_stl(facets)
            f.write("\n".join(lines))
        else: 
            data = self._build_binary_stl(facets)
            f.write("".join(data))

        f.close()

    def writeFEPOINT(self, file_name): 
        """writes out a new FEPOINT file with the given name, using the supplied points.
        derivs is of size (3,len(points),len(control_points)), giving matricies of 
        X,Y,Z drivatives

        jacobian should have a shape of (len(points),len(control_points))"""
        
        points = []
        triangles = []
        i_offset = 0
        for c in self._comps:
            print c.name
            points.extend(c.coords.cartesian)
            size = len(points)
            triangles.extend(c.stl.triangles + i_offset + 1) #tecplot wants 1 bias index, so I just increment here
            i_offset += size

        n_points = len(points)
        n_triangles = len(triangles)    

        derivs = None #TODO: FIX This in a minute

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
        for i,p in enumerate(points): 
            #TODO, also have to deal with derivatives here
            #Note: point counts are 1 bias, so I have to account for that with i
            line = "%.8f %.8f %.8f %d "%(p[0],p[1],p[2],i+1) 

            if derivs != None: 
                X = np.array(derivs[0][i,:])
                Y = np.array(derivs[1][i,:])
                Z = np.array(derivs[2][i,:])
                
                line += " ".join(('%.8f %.8f %.8f'%(x,y,z) for x,y,z in zip(X,Y,Z)))

            lines.append(line)

        for tri in triangles: 
            line = "%d %d %d %d"%(tri[0],tri[1],tri[2],tri[2])
            lines.append(line)


        f = open(file_name,'w')
        f.write("\n".join(lines))
        f.close()

