from model import Model
import random


m = random.random()*50
b = random.random()*50


X = [[random.random()*50] for x in range(10)]
Y = [[x[0]*m+b] for x in X]

def f(p,x):
	print(p)
	print(x)
	return p[0]*x[0]+p[1]
m = Model(f,[0,0])
m.opt.batch(X,Y)
