from numpy import linspace, hstack, dstack, less ,less_equal, logical_and, array,empty

class Bspline(object): 
    def __init__(self,controls,degree=3): #controls is a list of tuples  
        self.controls = controls
        self.degree = degree
        self.n = len(controls)
        self.knots =  hstack(([0,]*(self.degree-2),
                              hstack((linspace(0,1,self.n-degree+2),[1,]*(self.degree-1)))
                             ))
       
        
    def b_jn(self,j,n,t):         
        t_j   = self.knots[j-1]
        t_j1  = self.knots[j]
        t_jn  = self.knots[j+n-1]
        t_jn1 = self.knots[j+n]
        
        if n==0:       
            return logical_and(less_equal(t_j,t),less_equal(t,t_j1))  
        
        if t_jn-t_j:     
            q1 = (t-t_j)/(t_jn-t_j)
        else: 
            q1 = 0    
            
        if t_jn1-t_j1: 
            q2 = (t_jn1-t)/(t_jn1-t_j1)
        else: 
            q2 = 0
                    
        return q1*self.b_jn(j,n-1,t) + q2*self.b_jn(j+1,n-1,t)   
        
    def __call__(self,t): 
        X = sum([self.controls[i,0]*self.b_jn(i,self.degree-1,t) for i in range(0,self.n)])
        Y = sum([self.controls[i,1]*self.b_jn(i,self.degree-1,t) for i in range(0,self.n)])
        return dstack((X,Y))[0]
          
               