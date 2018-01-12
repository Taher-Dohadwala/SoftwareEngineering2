from multivariabledual import Dual
from math import sin
import sys

def tanh(x):
        return x-(x**3)/3+2*(x**5)/15-17*(x**7)/315+62*(x**9)/2835

def dense(X,p,activation=lambda x: tanh(x)):
        return [activation(X[i]*p[i*2]+p[i*2+1]) for i in range(len(X))]

def neuron(X,p,activation=lambda x: tanh(x)):
        return [activation(x*p[0]+p[1]) for x in X]


def loss(y,y1):
        return (y1-y)**2


X = [x/20.0 for x in range(100)]
Y = [sin(x/20.0) for x in range(100)]
ps = [Dual() for x in range(2)]
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
