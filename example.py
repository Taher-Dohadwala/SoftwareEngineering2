from multivariabledual import Dual

def f(x,m,b):
        return m*x+b
def loss(y,y1):
        #print("loss values", ((y1-y)**2).d, " with loss ", float((y1-y)**2))
        return (y1-y)**2
m = 2
b = 0
X = [x for x in range(20)]
Y = [f(x,m,b) for x in range(20)]
pm = Dual(x=1)
pb = Dual(x=1)
lr = 0.001
for i in range(20):
        o = 0
        for s in range(len(X)):
                o += loss(Y[s],f(X[s],pm,pb))
        pm.x-=(o[pm]/len(X))*lr
        pb.x-=(o[pb]/len(X))*lr
        print(pm.x,pb.x)
