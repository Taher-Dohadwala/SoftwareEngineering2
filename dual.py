class Dual:
	def __init__(self,x=1,d=1):
		self.x=x
		self.d=d
	def __add__(self,o):
		if (type(o)==Dual):
			x=self.x+o.x
			d=self.d+o.d
		else:
			x=self.x+o
			d=self.d
		return Dual(x=x,d=d)
	__radd__=__add__
	def __mul__(self,o):
		if (type(o)==Dual):
			x=self.x*o.x
			d=self.d*o.x+o.d*self.x
		else:
			x=self.x*o
			d=self.d*o
		return Dual(x=x,d=d)
	__rmul__=__mul__
	def __sub__(self,o):
		return self+(-1*o)
	def __rsub__(self,o):
		return (-1*self)+o
	def __pow__(self,o):
		if (type(o)==Dual):
			raise NotImplementedError("Power of a variable not implemented!")
		else:
			x=self.x**o
			d=o*self.d*self.x**(o-1)
		return Dual(x=x,d=d)
	def __rpow__(self,o):
		raise NotImplementedError("Power of a variable not implemented!")
	def __int__(self,o):
		return self.x
	def __str__(self):
		return str([self.x,self.d])

def small_angle_sine(x):
	return x-(1/6)*x**3+(1/120)*x**5-(1/5040)*x**7+(1/362880)*x**9

def dangerous_sine(x):
	t = int(x/3.141592653589793)
	return (1-2*(t%2))*small_angle_sine(x-(t*3.141592653589793))

if __name__=="__main__":
	import math
	print("Starting tests.")
	a = Dual()
	for x in range(-5,5):
		a.x=x
		assert (5*a*a*a+15).d == 15*(x**2)
		assert (5*a*a*a).x == 5*(x**3)
		assert (a+a).d == 2
		assert (a-a).d == 0
		assert (1-a).x == 1-x
		assert (5*(a**3)+15).d == 15*(x**2)
	print("Tests passed!")
	print("Our implementation of sine is inaccurate by an max of ~" + str(max([abs(math.sin(x/10.0)-dangerous_sine(x/10.0)) for x in range(-100,100)])) + ".")
