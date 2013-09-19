import struct
import string

import numpy as np
from scipy.sparse import csr_matrix

from stl import ASCII_FACET, BINARY_HEADER, BINARY_FACET

from ffd import Body, Shell


class Geometry(object): 

    def __init__(self): 

        self._comps = []
        self._i_comps = {}
        self._n_comps = 0 

        self._needs_linerize = True


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
        comp.name = name
        self._i_comps[name] = self._n_comps
        self._comps.append(comp)
        self._n_comps += 1

        self._needs_linerize = True


    def get_parameters(self): 
        """ returns a dictionary of parameters sets key'd to component names"""
        
        params = {}
        for comp in self._comps: 
            name = comp.name
            if isinstance(comp, Body): 
                params['%s.thickness'%name] = comp.C_bar
            else: 
                params['%s.thickness'%name] = comp.Cc_bar
                params['%s.centerline'%name] = comp.Ct_bar


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

    def _linearize(self): 
        if not self._needs_linerize: 
            return 

        points = []
        triangles = []
        i_offset = 0
        offsets = []
        n_controls = 0
        deriv_offsets = []
        for comp in self._comps:
            offsets.append(i_offset)
            deriv_offsets.append(n_controls)
            if isinstance(comp,Body): 
                points.extend(comp.stl.points)
                size = len(points)
                triangles.extend(comp.stl.triangles + i_offset + 1) #tecplot wants 1 bias index, so I just increment here
                i_offset = size
                n_controls += 2*comp.n_controls #X and R for each control point
            else: 
                points.extend(comp.outer_stl.points)
                size = len(points)
                triangles.extend(comp.outer_stl.triangles + i_offset + 1) #tecplot wants 1 bias index, so I just increment here
                i_offset = size
                n_controls += 2*comp.n_c_controls #X and R for each control point

                points.extend(comp.inner_stl.points)
                size = len(points)
                triangles.extend(comp.inner_stl.triangles + i_offset + 1) #tecplot wants 1 bias index, so I just increment here
                i_offset = size
                n_controls += comp.n_t_controls # only R for each control point

        self.points = points
        self.n_points = len(points)
        self.triangles = triangles
        self.n_triangles = len(triangles)
        self.offsets = offsets
        self.deriv_offsets = deriv_offsets

        i_comp = 0 #keep track of which comp the points came from
        comp = self._comps[0]
        i_offset=0
        i_deriv_offset = 0
        Jdata = []
        Jrow = []
        Jcolumn = []
        for i,p in enumerate(points): 

            #map point index to proper component
            if (i_comp < len(self._comps)-1) and (i == offsets[i_comp+1]): #the offset for the next comp: 
                i_offset = i
                i_comp += 1
                i_deriv_offset = deriv_offsets[i_comp]
                comp = self._comps[i_comp]


            deriv_values = np.zeros((3*n_controls,))
            
            if isinstance(comp,Body): 
                #x value
                start = i_deriv_offset
                end = start + 3*comp.n_controls
                #X is only a function of the x  parameter
                X = np.array(comp.dXqdC[i-i_offset,:])
                deriv_values[start:end:3] = X.flatten()  

                #r value
                start = end
                end = start + 3*comp.n_controls
                #Y,Z are only a function of the r parameter
                Y = np.array(comp.dYqdC[i-i_offset,:])
                Z = np.array(comp.dZqdC[i-i_offset,:])
                deriv_values[start+1:end:3] = Y.flatten() 
                deriv_values[start+2:end:3] = Z.flatten() 
            else: 
                #centerline x value
                start = i_deriv_offset
                end = start + 3*comp.n_c_controls
                #determine if point is on upper or lower surface? 
                outer=True
                deriv_i = i-i_offset
                if i-i_offset >= comp.n_outer: 
                    outer=False
                    deriv_i = i-i_offset-comp.n_outer

                #X is only a function of the x  parameter
                if outer: 
                    X = np.array(comp.dXoqdCc[deriv_i,:])
                else: 
                    X = np.array(comp.dXiqdCc[deriv_i,:])

                deriv_values[start:end:3] = X.flatten()  

                #centerline r value
                start = end
                end = start + 3*comp.n_c_controls
                #Y,Z are only a function of the r parameter
                if outer: 
                    Y = np.array(comp.dYoqdCc[deriv_i,:])
                    Z = np.array(comp.dZoqdCc[deriv_i,:])
                else: 
                    Y = np.array(comp.dYiqdCc[deriv_i,:])
                    Z = np.array(comp.dZiqdCc[deriv_i,:])
                deriv_values[start+1:end:3] = Y.flatten() 
                deriv_values[start+2:end:3] = Z.flatten() 

                #thickness parameter
                start = end
                end = start + 3*comp.n_t_controls
                if outer: 
                    Y = np.array(comp.dYoqdCt[deriv_i,:])
                    Z = np.array(comp.dZoqdCt[deriv_i,:])
                else: 
                    Y = np.array(comp.dYiqdCt[deriv_i,:])
                    Z = np.array(comp.dZiqdCt[deriv_i,:])

                deriv_values[start+1:end:3] = Y.flatten() 
                deriv_values[start+2:end:3] = Z.flatten() 

            Jdata.append(deriv_values)
        self.J = np.array(Jdata)
        self._needs_linerize = False

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
        
        self._linearize()
  
        
        lines = ['TITLE = "FFD_geom"',]
        var_line = 'VARIABLES = "X" "Y" "Z" "ID" '

        
        deriv_names = []
        deriv_tmpl = string.Template('"dx_d${name}_${type}$i" "dy_d${name}_${type}$i" "dz_d${name}_${type}$i"')
        for comp in self._comps: 
            if isinstance(comp,Body): 
                deriv_names.extend([deriv_tmpl.substitute({'name':comp.name,'i':str(i),'type':'X_'}) for i in xrange(0,comp.n_controls)]) #x,y,z derivs for each control point
                deriv_names.extend([deriv_tmpl.substitute({'name':comp.name,'i':str(i),'type':'R_'}) for i in xrange(0,comp.n_controls)]) #x,y,z derivs for each control point
            else: 
                deriv_names.extend([deriv_tmpl.substitute({'name':comp.name,'i':str(i),'type':'CX_'}) for i in xrange(0,comp.n_c_controls)]) #x,y,z derivs for each control point
                deriv_names.extend([deriv_tmpl.substitute({'name':comp.name,'i':str(i),'type':'CR_'}) for i in xrange(0,comp.n_c_controls)]) #x,y,z derivs for each control point
                deriv_names.extend([deriv_tmpl.substitute({'name':comp.name,'i':str(i),'type':'T_'}) for i in xrange(0,comp.n_t_controls)]) #x,y,z derivs for each control point

        var_line += " ".join(deriv_names)

        lines.append(var_line)

        lines.append('ZONE T = group0, I = %d, J = %d, F=FEPOINT'%(self.n_points,self.n_triangles)) #TODO I think this J number depends on the number of variables
        
        for i,p in enumerate(self.points): 
            line = "%.8f %.8f %.8f %d "%(p[0],p[1],p[2],i+1) #x,y,z,index coordiantes of point

            deriv_values = self.J[i]
            
            line += " ".join(np.char.mod('%.8f',deriv_values))

            lines.append(line)

        for tri in self.triangles: 
            line = "%d %d %d %d"%(tri[0],tri[1],tri[2],tri[2])
            lines.append(line)


        f = open(file_name,'w')
        f.write("\n".join(lines))
        f.close()

    def project_profile(self): 
        self._linearize()

        point_sets = []
        for comp in self._comps: 
            if isinstance(comp,Body):
                points = []
                for p in comp.stl.points: 
                    if abs(p[2]) < .0001 and p[1] > 0 : 
                        points.append(p)
                points = np.array(points)
                points = points[points[:,0].argsort()]
                point_sets.append(points)
            else: 
                points = []
                for p in comp.outer_stl.points: 
                    if abs(p[2]) < .0001 and p[1] > 0 : 
                        points.append(p)
                points = np.array(points)
                points = points[points[:,0].argsort()]
                point_sets.append(points)

                points = [] 
                for p in comp.inner_stl.points: 
                    if abs(p[2]) < .0001 and p[1] > 0 : 
                        points.append(p)
                points = np.array(points)
                points = points[points[:,0].argsort()]
                point_sets.append(points)

        return point_sets


