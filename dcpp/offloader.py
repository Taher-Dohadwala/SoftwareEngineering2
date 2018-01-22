import gc
import subprocess
import time

class Offloader:
	prog = ""
	instances = []
	occupied = []
	constants = {}
	maxalloc = 0
	def get_instance(self):
		a = OffloadInstance(self)
		self.instances.append(a)
		return a
	def update_occupied_array(self):
		tmp = []
		self.occupied=[]
		for i in self.instances:
			if(len(gc.get_referrers(i))==2): # we're the only ones who have this (i, self.instances)
				tmp.append(i)
			else:
				self.occupied.append(i.alloc)
		self.occupied+=list(self.constants.values())
		if (self.maxalloc<len(self.occupied)):
			self.maxalloc = len(self.occupied)
		for i in tmp:
			self.instances.remove(i)
	def allocate_slot(self):
		self.update_occupied_array()
		x = 0
		while(x in self.occupied):
			x+=1
		return x
	def compile(self,outputs):
		# ok step one tell the program how much memory we need in total
		self.cprog="h"+ str(self.maxalloc+1) + " " + self.prog
		# step two print out everything the user just asked for
		for i in outputs:
			self.cprog+=str(i.alloc) + " g "
		self.cprog+=" e"
		return self.cprog
	def run(self,inputs):
		if (not hasattr(self,"cprog")):
			raise Exception("Program not compiled!")
		t = time.time()
		p = subprocess.Popen(["./offload"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		print("%f seconds runtime. " % (time.time()-t))
		return [float(x) for x in str(p.communicate(input=bytes(self.cprog%tuple(inputs),encoding="ascii"))[0],encoding="ascii")[:-1].split("\n")]

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



if __name__=="__main__":
	o = Offloader()
	a = o.get_instance()
	b = 1
	for x in range(10):
		a+=x
		b+=x
	print(b)
	o.compile([a])
	print(o.run([1]))














