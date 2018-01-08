import numpy as np

def lengthmap(x,lengths={},root=True):
	if (hasattr(x,"__iter__")):
		lengths[id(x)] = sum([lengthmap(i,root=False) for i in x])
		return lengths if root else lengths[id(x)]
	else:
		return 1
def getindex(a,n,lengths):
	acc = 0
	for x in a:
		if (hasattr(x,"__iter__")):
			if (lengths[id(x)]+acc>n):
				return getindex(x,n-acc,lengths)
			acc+=lengths[id(x)]
		else:
			if (acc==n):
				return x
			acc+=1

a = [1,2,3,[4,5,6],7,[8,[9],[[10]]]]
l = lengthmap(a)
for x in range(10):
	print(getindex(a,x,l))
