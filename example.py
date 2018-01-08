import random
from multivariabledual import Dual

m = random.random()*50
b = random.random()*50


X = [1,2,3,4,5,6,7,8,9,10]
Y = [1.001,2.001,3.001,4.001,5.001,6.001,7.001,8.001,9.001,10.001]

def loss(YL,Y):
	return sum([(abs(Y[x]-YL[x])*0.1)**2 for x in range(len(YL))])*(1/len(YL))

def model(P,X):
	return [P[0]*x+P[1] for x in X]

def derivative(m,l,P,X,Y):
	P = [Dual(x=x) for x in P]
	r = l(Y,m(P,X))
	D = [r[x] for x in P]
	return D

p = [0,0]
for x in range(10):
	d = derivative(model,loss,p,X,Y)
	p = [p[x]-d[x]*0.001 for x in range(len(p))]
	print(str(d) + " : " + str(loss(Y,model(p,X))) + " : " + str(p))
