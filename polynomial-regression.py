from multivariabledual import Dual
from math import sin
def f(X,p):
        return sum([X*x**(j+1) for j,x in enumerate(p)])
def loss(y,y1):
                return (y1-y)**2

X = [x for x in range(20)]
Y = [sin(x) for x in range(20)]
ps = [Dual() for x in range(5)]
lr = 0.00001
o = 0
for i in range(200000):
        o = 0
        for s in range(5):
                try:
                        o += loss(Y[s],f(X[s],ps))
                except:
                        continue
        #print(float(o))
        for p in ps:
                p.x-=o[p]/len(X)*lr

print(float(o))
