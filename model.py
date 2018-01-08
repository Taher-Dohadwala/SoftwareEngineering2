from multivariabledual import Dual

def dualderiv(m,l,P,X,Y):
	P = [Dual(x=x) for x in P]
	r = l(Y,m(P,X))
	D = [r[x] for x in P]
	return D

def awfulderiv(m,l,P,X,Y):
	d = 0.01
	D = []
	b4 = l(Y,m(P,X))
	for p in range(len(P)):
		tp = P.copy()
		tp[p]+=d
		tpm = P.copy()
		tpm[p]-=d
		D.append(((l(Y,m(tp,X))-b4)/d-(l(Y,m(tpm,X))-b4)/d)/2)
	return D



class GradientDescent:
	def __init__(self,m,derivative=dualderiv,loss=lambda Y,YL: sum([abs(Y[x]-YL[x])**2 for x in range(len(YL))])/len(YL)):
		self.d=derivative
		self.m=m
		self.loss=loss
	def __init__(self,derivative=dualderiv,loss=lambda Y,YL: sum([abs(Y[x]-YL[x])**2 for x in range(len(YL))])/len(YL)):
		self.loss=loss
		self.d=derivative
		self.m=None
	def derive(self,x,y):
		return self.d(self.m,self.loss,self.m.weights,x,y)
	def batch(self,X,Y,lr=0.001):
		lr = lr/len(X)
		for s in zip(X,Y):
			o = self.derive(s[0],s[1])
			self.m.p = [self.m.p[x]-o[x]*lr for x in range(len(self.m.p))]
			
class Model():
	def __init__(self,f,p,optimizer=GradientDescent()):
		self.run=f
		self.weights=p
		optimizer.m=self
		self.opt=optimizer
	def __call__(self,X):
		return self.run(self.weights,X)
	def __call__(self,P,X):
		return self.run(P,X)
