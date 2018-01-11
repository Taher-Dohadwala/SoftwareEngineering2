class Dual:
	"""
	This object implements forwards differentiation with respect to multiple variables
	"""
	def __init__(self,x=1,d=1,respect=None):
		self.respect = id(self) if respect==None else respect
		self.x = x # the 'actual' value of this object.
		if (type(d)==int):
			self.d={self:d}
		else:
			self.d=d
	def processderivs(self,o,l):
		# this is a helpful little macro i've made.
		# takes: another dual object, a lambda taking four arguments.
		# this function will merge two dictionaries.
		# if there is a collision between the two dictionaries, the lambda given by the user is called to combine the two collisions in some way.
		d = {}
		for v in self.d.keys():
			if (v in o.d.keys()):
				d[v] = l(self.x,self.d[v],o.x,o.d[v])
			else:
				d[v] = self.d[v]
		for v in o.d.keys():
			if (not v in self.d.keys()):
				d[v] = o.d[v]
		return d
	def __add__(self,o):
		if (type(o)==Dual):
			x=self.x+o.x
			d=self.processderivs(o,lambda x1,d1,x2,d2: d1+d2)
		else:
			x=self.x+o
			d=self.d
		return Dual(x=x,d=d)
	__radd__=__add__
	def __mul__(self,o):
		if (type(o)==Dual):
			x=self.x*o.x
			d=self.processderivs(o,lambda x1,d1,x2,d2: x1*d2+x2*d1)
		else:
			x=self.x*o
			d={k:v*o for k,v in self.d.items()}
		return Dual(x=x,d=d)
	__rmul__=__mul__
	def __abs__(self):
		x = abs(self.x)
		d = {k:abs(v) for k,v in self.d.items()}
		return Dual(x=x,d=d)
	def __sub__(self,o):
		return self+(-1*o)
	def __rsub__(self,o):
		return (-1*self)+o
	def __pow__(self,o):
		if (type(o)==Dual):
			raise NotImplementedError("Power of a variable not implemented!")
		else:
			#print(self.x,"^", o)
			x = self.x**o
			t = self.x**(o-1)
			d = {k:o*v*t for k,v in self.d.items()}
		return Dual(x=x,d=d)
	def __truediv__(self,other):
		return self*(other**(-1))
	def __rpow__(self,o):
		raise NotImplementedError("Power of a variable not implemented!")
	def __int__(self):
		return int(self.x)
	def __float__(self):
		return float(self.x)
	def __str__(self):
		return str([self.x,self.d])
	def __getitem__(self,x):
		if (type(x)==Dual):
			try:
				return self.d[x]
			except KeyError:
				return 0
def small_angle_sine(x):
	return x-(1/6)*x**3+(1/120)*x**5-(1/5040)*x**7+(1/362880)*x**9

def dangerous_sine(x):
	t = int(x/3.141592653589793)
	return (1-2*(t%2))*small_angle_sine(x-(t*3.141592653589793))

if __name__=="__main__":
	import math
	print("Starting tests.")
	a = Dual()
	b = Dual()
	c = Dual()
	c.x=-2
	for x in range(-5,5):
		a.x=x
		b.x=x
		assert (5*a*a*a*b+15+b)[a] == 15*(x**2)
		assert (5*a*a*a*b).x == 5*(x**3)*x
		assert (a+a-b)[a] == 2
		assert (b+a-a-b)[a] == 0
		assert (1-a).x == 1-x
		assert (5*(a**3)+15)[a] == 15*(x**2)
		print(((c-b)**2)[b])
	print("Tests passed!")
	print("Our implementation of sine is inaccurate by an max of ~" + str(max([abs(math.sin(x/10.0)-dangerous_sine(x/10.0)) for x in range(-100,100)])) + ".")
