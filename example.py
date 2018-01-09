from multivariabledual import Dual

def f(x,m,b):
def loss(y,y1):
        return abs(y-y1)**2
m = 5
b = -5
X = [x for x in range(20)]
Y = [f(x,m,b) for x in range(20)]
pm = Dual(x=1)
pb = Dual(x=1)
pmacc = 0
pbacc = 0

for i in range(100):
        for s in range(len(X)):
                o = loss(Y[s],f(X[s],pm,pb))
                pmacc+=o[pm]
                pbacc+=o[pb]
        pmacc= float(pmacc)/len(X)
        pbacc= float(pbacc)/len(X)
        pm.x-=pmacc*0.001
        pb.x-=pbacc*0.001
        print(pmacc,pbacc)
