from multivariabledual import Dual

class linear_classifier:

    def __init__(self):
        self.m = 0
        self.b = 0
        self.grad_hist = []
        self.lr = 0.001
        


    def Model(self,X,Y):
        self.x = X
        self.y = Y
        # y = mx+b
        return self.m*self.x + self.b

    def loss(self):
        return (y1-y)**2

    def fit_squaredError(self):
        self.pm = Dual(x=1)
        self.pb = Dual(x=1)

        for i in range(20):

            o = 0

            for s in range(len(self.x)):
                o += loss(self.y[s],Model(self.x[s])

                

        
        
        

        
        
        
