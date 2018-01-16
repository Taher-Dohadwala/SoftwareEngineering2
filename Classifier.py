from multivariabledual import Dual

class linear_classifier:

    def __init__(self):
        self.m = 1
        self.b = 0
        self.grad_hist = []
        


     #support functions that does all the calculations
    def f(self,X):
        self.x = X
        # y = mx+b
        return self.m*self.x + self.b

    def loss(self,y,y1):
        return (y1-y)**2



    # parameters such as choosing loss function and optimizer
    def compile(self,loss,optimizer, lr=0.001):
        self.lr = lr
        

    # trains data based on loss function and optimizer
    def fit(self,x_train,y_train, epochs=10):
        self.y = y_train
        self.pm = Dual(x=1)
        self.pb = Dual(x=1)
        

        for i in range(epochs):
            o = 0

            for s in range(len(x_train)):
                o += self.loss(y_train[s],self.f(x_train[s]))
                print(o)

        
            self.pm.x -= (o/len(x_train))*self.lr
            self.pb.x -= (o/len(x_train))*self.lr
            print ("m:",str(self.pm.x) + " : "+ "b:",str(self.pb.x))
    

    def predict(self):
        pass

        
        
        

        
        
        
