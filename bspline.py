from numpy import linspace, hstack, dstack, less ,less_equal, logical_and, \
    array, empty, matrix, dot
    
from scipy.optimize import newton as fsolve
from scipy.sparse import csr_matrix

class Bspline(object): 
    def __init__(self,controls,points,order=3): #controls is a list of tuples  
        self.controls = controls
        self.order = order
        self.degree = order-1
        self.n = len(controls)
        self.knots =  hstack(([0,]*(self.degree),
                              hstack((linspace(0,1,self.n-self.order+2),[1,]*(self.degree)))
                             ))
         
                          
        #pre-calculate the B matrix
        n_p = points.shape[0]
        self.B = matrix(empty((n_p,self.n)))
        
        for i,p in enumerate(points): 
            t = self.find(p)
            for j in range(0,self.n): 
                self.B[i,j] = self.b_jn_wrapper(j,self.degree,t)
        self.B = csr_matrix(self.B)        
    def calc(self,C):
        return array(self.B.dot(C))                                   
     
    def find(self,X):
        """returns the parametric coordinate that matches the given x location""" 
        
        def func(x,target=0):
            return self(x)[:,0] - target
        try:     
            return array([fsolve(lambda f:func(f,x),[0,]) for x in X])[:,0]
        except TypeError:
            return fsolve(lambda f:func(f,X),[0,])   
        
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
        rng = range(0,self.n)
        b = [self.b_jn_wrapper(i,self.degree,t) for i in rng]
        X = dot(self.controls[:,0],b)
        Y = dot(self.controls[:,1],b)
        return dstack((X,Y))[0]
        
        
 
          
               