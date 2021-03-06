from multivariabledual import Dual
from math import sin
import sys

def f(X,p):
        return sum([X*x**(j+1) for j,x in enumerate(p)])
def loss(y,y1):
        return (y1-y)**2

X = [x/20.0 for x in range(100)]
Y = [sin(x/20.0) for x in range(100)]
ps = [Dual() for x in range(5)]
lr = 0.001
o = 0
e = 1000
for i in range(e):
        o = 0
        for s in range(len(X)):
                try:
                        o += loss(Y[s],f(X[s],ps))
                except:
                        continue
        for p in ps:
                p.x-=o[p]/len(X)*lr
        if (i%(e/10)==0):
                print(o.x)
print(float(o))
print([float(p) for p in ps])
