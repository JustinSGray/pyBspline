import numpy as np

from bspline import Bspline


class Body(object): 
    """FFD class for solid bodyies which only have one surface""" 
    
    def __init__(self,geom_points,control_points): 
    
        self.P = geom_points
        self.P_bar = geom_points.copy()
        self.C = control_points  
        self.bs = Bspline(control_points,geom_points)
        
        self.r_mag = np.average(geom_points[:,1])

    def deform(self,delta_C): 
        """returns new point locations for the given motion of the control 
        points"""         
        self.C_bar = self.C+delta_C
        
        delta_P = self.bs.calc(self.C_bar)
        self.P_bar = self.P.copy()
        self.P_bar[:,0] = delta_P[:,0]
        self.P_bar[:,1] = self.P[:,1]+self.r_mag*delta_P[:,1] 
        
        #calculate derivatives
        self.dPx_barqdC = self.bs.B
        self.dPr_bardC = self.r_mag*self.bs.B
       
        return self.P_bar
                    
        
class Shell(object): 
    """FFD class for shell bodies which have two connected surfaces"""
    
    def __init__(self,upper_points,lower_points,center_iine_controls,thickness_controls): 
    
        self.Po = upper_points
        self.Pi = lower_points
        self.Po_bar = upper_points.copy()
        self.Pi_bar = lower_points.copy()
        
        self.Cc = center_iine_controls
        self.Ct = thickness_controls 
         
        self.bsc_o = Bspline(self.Cc,upper_points)
        self.bsc_i = Bspline(self.Cc,lower_points)
        
        self.bst_o = Bspline(self.Ct,upper_points)
        self.bst_i = Bspline(self.Ct,lower_points)
        
        self.r_mag = np.average(upper_points[:,1])

        #for revolution of 2-d profile
        self.n_theta = 20

        self.Theta = np.linspace(0,2*np.pi,self.n_theta)
        self.ones = np.ones(self.n_theta)
        self.sin_theta = np.sin(self.Theta)
        self.cos_theta = np.cos(self.Theta)

        #calculate derivatives
        #in polar coordinates
        self.dPo_bar_xqdCc = self.bsc_o.B.flatten()
        self.dPo_bar_rqdCc = self.r_mag*self.bsc_o.B.flatten()

        self.dPi_bar_xqdCc = self.bsc_i.B.flatten()
        self.dPi_bar_rqdCc = self.r_mag*self.bsc_i.B.flatten()

        self.dPo_bar_rqdCt = self.r_mag*self.bst_o.B.flatten()
        self.dPi_bar_rqdCt = -1*self.r_mag*self.bst_i.B.flatten()

        #Project Polar derivatives into revolved cartisian coordinates
        self.dXoqdCc = np.outer(self.dPo_bar_xqdCc,self.ones)
        self.dYoqdCc = np.outer(self.dPo_bar_rqdCc,self.sin_theta)
        self.dZoqdCc = np.outer(self.dPo_bar_rqdCc,self.cos_theta)

        self.dXiqdCc = np.outer(self.dPi_bar_xqdCc,self.ones)
        self.dYiqdCc = np.outer(self.dPi_bar_rqdCc,self.sin_theta)
        self.dZiqdCc = np.outer(self.dPi_bar_rqdCc,self.cos_theta)

        self.dYoqdCt = np.outer(self.dPo_bar_rqdCt,self.sin_theta)
        self.dZoqdCt = np.outer(self.dPo_bar_rqdCt,self.cos_theta)
        self.dYiqdCt = np.outer(self.dPi_bar_rqdCt,self.sin_theta)
        self.dZiqdCt = np.outer(self.dPi_bar_rqdCt,self.cos_theta)

            

    def deform(self,delta_Cc,delta_Ct): 
        """returns new point locations for the given motion of the control 
        points for center-line and thickness"""      
        
        self.Cc_bar = self.Cc+delta_Cc
        delta_Pc_o = self.bsc_o.calc(self.Cc_bar)
        delta_Pc_i = self.bsc_i.calc(self.Cc_bar)
        
        self.Ct_bar = self.Ct+delta_Ct
        delta_Pt_o = self.bst_o.calc(self.Ct_bar)
        delta_Pt_i = self.bst_i.calc(self.Ct_bar)

        self.Po_bar = self.Po.copy()
        self.Pi_bar = self.Pi.copy()
        
        self.Po_bar[:,0] = delta_Pc_o[:,0]
        self.Po_bar[:,1] = self.Po[:,1]+self.r_mag*(delta_Pc_o[:,1]+delta_Pt_o[:,1])
        
        self.Pi_bar[:,0] = delta_Pc_i[:,0]
        self.Pi_bar[:,1] = self.Pi[:,1]+self.r_mag*(delta_Pc_i[:,1]-delta_Pt_i[:,1])
        
        
        #Perform axial roation of 2-d polar coordiantes
        #outer surface
        Po_bar_r = self.Po_bar[:,1]
        self.Xo = np.outer(self.Po_bar[:,0],self.ones)
        self.Yo = np.outer(Po_bar_r,self.sin_theta)
        self.Zo = np.outer(Po_bar_r,self.cos_theta)

        #inner surface
        Pi_bar_r = self.Pi_bar[:,1]
        self.Xi = np.outer(self.Pi_bar[:,0],self.ones)
        self.Yi = np.outer(Pi_bar_r,self.sin_theta)
        self.Zi = np.outer(Pi_bar_r,self.cos_theta)


        return self.Po_bar,self.Pi_bar


        