import numpy as np
class linear:
	def __init__(self):
		self.weights=[0,0]
	def run(x):
		return self.weights[0]*x+self.weights[1]

def dumbsum(a):
	acc = a[0]
	for x in a[1:]:
		acc = acc + x
	return acc

def simplifycount(a):
	if (not hasattr(a,"__iter__")):
		return [1]
	return [dumbsum([lengthmap(x) for x in a])]

class Lengthling:
	def __init__(self,v,p):
		self.v = v
		self.p = p
	def __str__(self):
		return str(self.v) + " values at " + str()
	def __int__(self):
		return self.v

def lengthmap(a):
	acc = 0
	accl = []
	for x in a:
		if (not hasattr(x,"__iter__")):
			acc+=1
		else:
			if (acc>0):
				accl.append(acc)
				acc = 0
			accl.append(lengthmap(x))
	if (acc>0):
		accl.append(acc)
	return accl

def undex(a,b):
	if (b==[]):
		return a
	return undex(a[b[0]],b[1:])

def smartsum(x):
	if (not hasattr(x,"__iter__")):
		return x
	return sum([smartsum(i) for i in x])


def getindex(a,n):
	acc = 0
	rcounter = 0
	for x in a:
		if (hasattr(x,"__iter__")):
			t = n-acc
			t2 = getindex(x,t)
			if (t2[0]==t):
				return [rcounter] + t2
			acc+=t2[0]
		else:
			if (acc+x>=n):
				return [n]
			acc+=x
			rcounter+=x
	return [acc]

class Linearized:
	def __init__(self,x):
		self.raw = x
		self.lengthmap = lengthmap(x)
		self.length = smartsum(self.lengthmap)

	"""def __getindex__(self,n):
		if (n>self.length-1):
			return None
		acc = 0
		while (n<acc):"""


a = lengthmap([1,2,3,[1,2,3],np.zeros([3,3])])
for x in range(15):
	print(getindex(a,x+1))







