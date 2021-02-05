import numpy as np

'''
print("")
print("TEST:")
print()
print()
print("")
'''

def valueInGroup(value, group):
	try:
		test = group[value]
		return True
	except:
		return False
#end valueInGroup

def σ(V):
	# range is 1 to -1
	# uses hyperbolic tangent
	V = float(V)
	num = 1/(1 + np.exp(-V))
	return num
#end σ

#print(σ(1))