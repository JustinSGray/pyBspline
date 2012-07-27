from numpy import linspace, hstack, dstack, less ,less_equal, logical_and, array,empty
from scipy.optimize import fsolve

class Bspline(object): 
    def __init__(self,controls,order=3): #controls is a list of tuples  
        self.controls = controls
        self.order = order
        self.degree = order-1
        self.n = len(controls)
        self.knots =  hstack(([0,]*(self.degree),
                              hstack((linspace(0,1,self.n-self.order+2),[1,]*(self.degree)))
                             ))
     
    def map(self,X):
        """returns the parametric coordinate that matches the given x location""" 
        
        def func(x,target=0):
            return self(x)[:,0] - target
        try:     
            return array([fsolve(func,[0,],args=(x,)) for x in X])[:,0]
        except TypeError:
            return fsolve(func,[0,],args=(X,))   
        
    def b_jn(self,j,n,t):         
        t_j   = self.knots[j]
        t_j1  = self.knots[j+1]
        t_jn  = self.knots[j+n]
        t_jn1 = self.knots[j+n+1]
        
        if n==0:       
            return logical_and(less_equal(t_j,t),less(t,t_j1))                
        
        if t_jn-t_j:     
            q1 = (t-t_j)/(t_jn-t_j)
        else: 
            q1 = 0    
            
        if t_jn1-t_j1: 
            q2 = (t_jn1-t)/(t_jn1-t_j1)
        else: 
            q2 = 0
                
        B = q1*self.b_jn(j,n-1,t) + q2*self.b_jn(j+1,n-1,t)   
        
        return B
        
    #dirty hack to fix some weird corner case that shows up    
    def b_jn_wrapper(self,j,n,t): 
        B = self.b_jn(j,n,t)
        if j == self.n-1: 
            B[t==1]=1 #anywhere t=1, set B = 1
        return B 
        
    def __call__(self,t): 
        X = sum([self.controls[i,0]*self.b_jn_wrapper(i,self.degree,t) for i in range(0,self.n)])
        Y = sum([self.controls[i,1]*self.b_jn_wrapper(i,self.degree,t) for i in range(0,self.n)])
        return dstack((X,Y))[0]
        
        
 
          
               