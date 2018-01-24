import gc
import subprocess
import time
import random
import timeit
import sys

class Offloader:
	def __init__(self):
		self.prog = []
		self.instances = []
		self.occupied = []
		self.constants = {}
		self.maxalloc = 0
	def get_instance(self):
		a = OffloadInstance(self)
		self.instances.append(a)
		return a
	def garbage_collect(self):
		tmp = []
		for i in self.instances:
			gc.collect()
			if(len(gc.get_referrers(i))==2): # we're the only ones who have this (i, self.instances)
				tmp.append(i)
		for i in tmp:
			self.instances.remove(i)
		self.update_occupied_array()

	def update_occupied_array(self): # needs to be redone
		self.occupied=[]
		for i in self.instances:
			self.occupied.append(i.alloc)
		self.occupied+=list(self.constants.values())
		if (self.maxalloc<len(self.occupied)):
			self.maxalloc = len(self.occupied)

	def allocate_slot(self):
		self.update_occupied_array()
		x = 0
		while(x in self.occupied):
			x+=1
		return x
	def compile(self):
		self.garbage_collect()
		# ok step one tell the program how much memory we need in total
		self.cprog="h"+ str(self.maxalloc+1) + " " + " ".join(self.prog)
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
			self.instances[x].v = tmp[x]
	def __getitem__(self,v):
		return self.outputs[v]

class OffloadInstance:
	def __init__(self,o,alloc=None):
		self.o = o
		self.alloc=alloc
		self.v = 0
		if (alloc==None): # we're an input.
			self.alloc = o.allocate_slot()
			self.o.prog.append(str(self.alloc) + " f%f") # allocate this value
			self.o.update_occupied_array()
	def get_opstring(self,d,i,op,i2): #redo for llvm once we know this works
		return str(d) + " " + str(i2) + " " + str(i) + " " + op
	def get_other_index(self,p):
		if (type(p)==int or type(p)==float):
			p = float(p)
			if (p in self.o.constants.keys()):
				return self.o.constants[p]
			else:
				i = self.o.constants[p] = self.o.allocate_slot()
				self.o.prog.append(str(i)+" f"+str(p)+" ") # allocate the constant
				return i
		elif(type(p)==OffloadInstance):
			return p.alloc
	def do_op(self,p,op,reverse=False):
		i = self.get_other_index(p)
		dst = self.o.allocate_slot()
		self.o.prog.append(self.get_opstring(dst,i,op,self.alloc) if reverse else self.get_opstring(dst,self.alloc,op,i))
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
	def __float__(self):
		return float(self.v)


def test_lambda(l):
	o = Offloader()
	print(l)
	l = eval(l)
	t2 = [o.get_instance() for x in range(l.__code__.co_argcount)]
	a = l(*t2)
	o.compile()
	print(o.cprog)
	for x in range(100):
		try:
			t1 = [random.randrange(-5,5) for x in range(l.__code__.co_argcount)]
			o.run(t1)
			tmp = float(a)-l(*t1)
			if (abs(tmp)>0.001):
				raise Exception(str(o.run(t1)[a]) + " vs. " + str(l(*t1)) + " for args " + str(t1))
		except ZeroDivisionError:
			pass
	print("Passed test.")

def test_function(f,params):
	o = Offloader()
	

def dot(a,b):
	acc = 0
	for xa in a:
		for xb in b:
			acc += xa*xb
		sys.stdout.write(".")
		sys.stdout.flush()

def dot_o(a,b,o):
	acc = 0
	for xa in a:
		for xb in b:
			acc += xa*xb
		o.garbage_collect()
		sys.stdout.write(".")
		sys.stdout.flush()

if __name__=="__main__":
	test_lambda("lambda x: x+1")
	test_lambda("lambda x,y: x+y")
	test_lambda("lambda x,y,z: x*y*z")
	test_lambda("lambda x: x**2")
	test_lambda("lambda x: x**5+1")
	test_lambda("lambda x,y: x/y")	
	test_lambda("lambda x,y,z: x**5+y/z")
	o = Offloader()
	dt = 50
	params = [random.randrange(-20,20) for x in range(dt)]
	t2 = [o.get_instance() for x in range(dt)]
	tmp = time.time()
	dot(params[0:int(dt/2)],params[int(dt/2):])
	print("python took %f seconds." %(time.time()-tmp))
	tmp = time.time()
	a = dot_o(t2[0:int(dt/2)],t2[int(dt/2):],o)
	o.compile()
	print("compiling took %f seconds." %(time.time()-tmp))
	tmp = time.time()
	o.run(params)
	print("running took %f seconds." %(time.time()-tmp))
	










