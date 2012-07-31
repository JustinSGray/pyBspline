import numpy as np

from bspline import Bspline


class Body(object): 
    """FFD class for solid bodyies which only have one surface""" 
    
    def __init__(self,geom_points,control_points): 
    
        self.P = geom_points
        self.P_bar = geom_points.copy()
        self.C = control_points  
        self.bs = Bspline(control_points,geom_points)
        
        self.y_mag = np.average(geom_points[:,1])

        
        
    def deform(self,delta_C): 
        """returns new point locations for the given motion of the control 
        points"""         
        self.C_bar = self.C+delta_C
        
        delta_P = self.bs.calc(self.C_bar)
        self.P_bar = self.P.copy()
        self.P_bar[:,0] = delta_P[:,0]
        self.P_bar[:,1] = self.P[:,1]+self.y_mag*delta_P[:,1] 
       
        return self.P_bar
          
            
        
class Shell(object): 
    """FFD class for shell bodies which have two connected surfaces"""
    
    def __init__(self,upper_points,lower_points,center_line_controls,thickness_controls): 
    
        self.Pu = upper_points
        self.Pl = lower_points
        self.Pu_bar = upper_points.copy()
        self.Pl_bar = lower_points.copy()
        
        self.Cc = center_line_controls
        self.Ct = thickness_controls 
         
        self.bsc_u = Bspline(self.Cc,upper_points)
        self.bsc_l = Bspline(self.Cc,lower_points)
        
        self.bst_u = Bspline(self.Ct,upper_points)
        self.bst_l = Bspline(self.Ct,lower_points)
        
        self.y_mag = np.average(upper_points[:,1])


        
    def deform(self,delta_Cc,delta_Ct): 
        """returns new point locations for the given motion of the control 
        points for center-line and thickness"""      
        
        self.Cc_bar = self.Cc+delta_Cc
        delta_Pc_u = self.bsc_u.calc(self.Cc_bar)
        delta_Pc_l = self.bsc_l.calc(self.Cc_bar)
        
        self.Ct_bar = self.Ct+delta_Ct
        delta_Pt_u = self.bst_u.calc(self.Ct_bar)
        delta_Pt_l = self.bst_l.calc(self.Ct_bar)

        self.Pu_bar = self.Pu.copy()
        self.Pl_bar = self.Pl.copy()
        
        self.Pu_bar[:,0] = delta_Pc_u[:,0]
        self.Pu_bar[:,1] = self.Pu[:,1]+delta_Pc_u[:,1]+delta_Pt_u[:,1]
        
        self.Pl_bar[:,0] = delta_Pc_l[:,0]
        self.Pl_bar[:,1] = self.Pl[:,1]+self.y_mag*(delta_Pc_l[:,1]-delta_Pt_l[:,1])
        
        return self.Pu_bar,self.Pl_bar
        