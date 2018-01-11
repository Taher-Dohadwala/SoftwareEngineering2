from multivariabledual import Dual

class linear_classifier:

    def __init__(self):
        self.m = 0
        self.b = 0
        self.grad_hist = []
        
        


    # parameters such as choosing loss function and optimizer
    def compile(self,loss,optimizer, lr=0.001):
        self.lr = lr
        pass

    # trains data based on loss function and optimizer
    def fit(self,x_train,y_train, epochs=10):
        self.pm = Dual(x=1)
        self.pb = Dual(x=1)

        for i in range(epochs):
            o = 0

            for s in range(len(x_train)):
                o += loss(y_train[s],f(x_train[s]))

            self.pm.x -= (o[self.pm]/len(x_train))*self.lr
            self.pb.x -= (o[self.pb]/len(x_train))*self.lr
            print ("m:",self.pm.x + " : "+ "b:",self.pb.x)
    

    def predict(self):
        pass

    
    #support functions that does all the calculations
    def f(self,X):
        self.x = X
        self.y = Y
        # y = mx+b
        return self.m*self.x + self.b

    def loss(self,y,y1):
        return (y1-y)**2


        
        
        

        
        
        
