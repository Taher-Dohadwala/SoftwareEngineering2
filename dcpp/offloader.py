import gc
import subprocess
import time
import random

"""
- generate a list of ids
- every instance remembers it's parent
- when trying to prove it shouldn't be saved, must also prove that there isn't a living ancestor.
"""

class Offloader:
	def __init__(self):
		self.prog = ""
		self.instances = []
		self.occupied = []
		self.constants = {}
		self.maxalloc = 0
		self.outputs = {}
		self.ids = []
	def get_instance(self):
		a = OffloadInstance(self)
		self.instances.append(a)
		return a

	def update_occupied_array(self): # needs to be redone
		tmp = []
		self.occupied=[]
		self.ids = [id(x) for x in self.instances]
		for i in self.instances:
			gc.collect()
			if(len(gc.get_referrers(i))==2 and not stack_scan(i)): # we're the only ones who have this (i, self.instances)
				tmp.append(i)
			else:
				self.occupied.append(i.alloc)
		self.occupied+=list(self.constants.values())
		if (self.maxalloc<len(self.occupied)):
			self.maxalloc = len(self.occupied)
		for i in tmp:
			self.instances.remove(i)
		print("occupation array updated: " + str(self.occupied))
		print(self.prog)
	def allocate_slot(self):
		self.update_occupied_array()
		x = 0
		while(x in self.occupied):
			x+=1
		return x
	def compile(self):
		self.update_occupied_array()
		# ok step one tell the program how much memory we need in total
		self.cprog="h"+ str(self.maxalloc+1) + " " + self.prog
		# step two print out everything the user just asked for
		for i in self.occupied:
			self.cprog+=str(i) + " g "
		self.cprog+="e"
		return self.cprog
	def run(self,inputs):
		if (not hasattr(self,"cprog")):
			self.compile()
		t = time.time()
		p = subprocess.Popen(["./offload"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		#print("%f seconds runtime. " % (time.time()-t))
		tmp = [float(x) for x in str(p.communicate(input=bytes(self.cprog%tuple(inputs),encoding="ascii"))[0],encoding="ascii")[:-1].split("\n")]
		for x in range(len(self.instances)):
			self.outputs[self.instances[x]] = tmp[x]
		return self.outputs
	def __getitem__(self,v):
		return self.outputs[v]

class OffloadInstance:
	def __init__(self,o,alloc=None):
		self.o = o
		self.alloc=alloc
		if (alloc==None): # we're an input.
			self.alloc = o.allocate_slot()
			self.o.prog += str(self.alloc) + " f%f " # allocate this value
	def get_opstring(self,d,i,op,i2): #redo for llvm once we know this works
		return str(d) + " " + str(i2) + " " + str(i) + " " + op + " "
	def get_other_index(self,p):
		if (type(p)==int or type(p)==float):
			p = float(p)
			if (p in self.o.constants.keys()):
				return self.o.constants[p]
			else:
				i = self.o.constants[p] = self.o.allocate_slot()
				self.o.prog+=str(i)+" f"+str(p)+" " # allocate the constant
				return i
		elif(type(p)==OffloadInstance):
			return p.alloc
	def do_op(self,p,op,reverse=False):
		i = self.get_other_index(p)
		dst = self.o.allocate_slot()
		self.o.prog+=self.get_opstring(dst,i,op,self.alloc) if reverse else self.get_opstring(dst,self.alloc,op,i)
		dsto = OffloadInstance(self.o,alloc=dst)
		self.o.instances.append(dsto)
		self.o.update_occupied_array()
		return dsto
	def __add__(self,p):
		return self.do_op(p,"+")
	__radd__=__add__
	def __mul__(self,p):
		return self.do_op(p,"*")
	__rmul__=__mul__
	def __truediv__(self,p):
		return self.do_op(p,"/")
	def __rtruediv__(self,p):
		return self.do_op(p,"/",reverse=True)
	def __sub__(self,p):
		return self.do_op(p,"-")
	def __rsub__(self,p):
		return self.do_op(p,"-",reverse=True)
	def __pow__(self,p):
		return self.do_op(p,"^")
	def __rpow__(self,p):
		return self.do_op(p,"^",reverse=True)


def test_lambda(l):
	o = Offloader()
	print("%d arguments." % (l.__code__.co_argcount))
	t2 = [o.get_instance() for x in range(l.__code__.co_argcount)]
	a = l(*t2)
	o.compile()
	print(o.cprog)
	for x in range(100):
		try:
			t1 = [random.randrange(-5,5) for x in range(l.__code__.co_argcount)]
			tmp = o.run(t1)[a]-l(*t1)
			if (abs(tmp)>0.001):
				raise Exception(str(o.run(t1)[a]) + " vs. " + str(l(*t1)) + " for args " + str(t1))
		except ZeroDivisionError:
			pass
	print("Passed test.")


if __name__=="__main__":
	test_lambda(lambda x: x+1)
	test_lambda(lambda x,y: x+y)
	test_lambda(lambda x,y,z: x*y*z)
	test_lambda(lambda x: x**2)
	test_lambda(lambda x: x**5+1)
	test_lambda(lambda x,y: x/y)	
	test_lambda(lambda x,y,z: x**5+y/z)













