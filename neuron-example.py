from multivariabledual import Dual
from math import sin
import sys
from time import time
import pickle

def tanh(x):
        return x-(x**3)/3+2*(x**5)/15-17*(x**7)/315+62*(x**9)/2835

def dense(X,p,activation=lambda x: tanh(x)):
        t = len(X)
        n = int(len(p)/(t+1))
        return [neuron(X,p[i*t:((i+1)*t)+1],activation=activation) for i in range(n)]

def neuron(X,p,activation=lambda x: tanh(x)):
        return activation(sum([X[x]*p[x+1] for x in range(len(X))])+p[0])

def loss(y,y1):
        return (y1-y)**2

def onehot_categorical_loss(y,y1):
        if (type(y1)==int):
                return oneshot_categorical_loss(y1,y)
        

tmpt = time()
X = pickle.load(open("C:\\Users\\tpreichel\\Desktop\\MNIST-dataset-in-different-formats-master\\data\\CSV format\\X.pk","rb"))
Y = pickle.load(open("C:\\Users\\tpreichel\\Desktop\\MNIST-dataset-in-different-formats-master\\data\\CSV format\\Y.pk","rb"))
print("loaded mnist in",time()-tmpt)

ps = [Dual() for x in range(7850)]
lr = 0.001
o = 0
e = 1000
"""for i in range(e):
        o = 0
        for s in range(len(X)):
                try:
                        o += loss(Y[s],neuron(X[s],ps,activation=lambda x:x))
                except:
                        continue
        for p in ps:
                p.x-=o[p]/len(X)*lr
        if (i%(e/10)==0):
                print(o.x)"""
print([float(x) for x in dense(X[0],ps)])
