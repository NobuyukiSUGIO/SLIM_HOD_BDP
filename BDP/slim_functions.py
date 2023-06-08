# -*- coding: utf-8 -*-

"""
Left 16 bits			Right 16 bits 
1st-round
(x0,x1,---,x15)			(x16,x17,---,x31)
		|						|
		XOR<---[P]<---[S]<------|
		|						|
		[		  SWAP  		]
		|						|
2nd-round
(x0,x1,---,x15)			(x16,x17,---,x31)
"""
def slim(n):
	"""--------------------------
	Create the constraints of slim
	--------------------------"""	
	model = "slim.lp"
	fileobj = open(model, "a")
	# copy
	for i in range(16):
		fileobj.write(("x" + str(i+16) + "_" + str(n-1) + " - sx" + str(i) + "_" + str(n) + " - x" + str(i) + "_" + str(n) + " = 0"))
		fileobj.write("\n")
	# xor
	PL = [7,13,1,8,11,14,2,5,4,10,15,0,3,6,9,12]
	for i in range(16):
		fileobj.write(("x" + str(i) + "_" + str(n-1) + " + sy" + str(PL[i]) + "_" + str(n) + " - x" + str(i+16) + "_" + str(n) + " = 0"))
		fileobj.write("\n")
	fileobj.close()

def S(n):
	"""
	Generate the constraints by sbox layer.
	"""
	# Linear inequalities for the SLIM Sbox
	S_T=[[1 ,  1 ,  1 ,  1 ,  0 ,  0 ,  0 , - 1 , 0],\
		[1 ,  1 ,  1 ,  1 ,  0 , - 1 ,  0 ,  0 , 0],\
		[1 ,  1 ,  1 ,  1 ,  0 ,  0 , - 1 ,  0 , 0],\
		[1 ,  1 ,  1 ,  1 , - 1 ,  0 ,  0 ,  0 , 0],\
		[0 ,  0 ,  0 , - 1 ,  1 ,  1 ,  1 ,  1 , 0],\
		[0 ,  0 , - 1 ,  0 ,  1 ,  1 ,  1 ,  1 , 0],\
		[0 , - 1 ,  0 ,  0 ,  1 ,  1 ,  1 ,  1 , 0],\
		[-1 ,  0 ,  0 ,  0 ,  1 ,  1 ,  1 ,  1 , 0],\
		[0 ,  0 ,  0 ,  0 ,  1 , - 1 , - 1 ,  0 , -1],\
		[0 ,  0 ,  0 ,  0 , - 1 , - 1 ,  1 ,  0 , -1],\
		[0 ,  0 ,  1 ,  0 , - 1 ,  0 , - 1 ,  0 , -1],\
		[0 ,  0 ,  0 ,  0 ,  1 ,  0 , - 1 , - 1 , -1],\
		[0 ,  0 ,  0 ,  0 , - 1 ,  0 ,  1 , - 1 , -1],\
		[0 , - 1 ,  0 , - 1 ,  0 ,  1 ,  0 , - 1 , -2],\
		[0 ,  1 ,  0 ,  0 , - 1 ,  0 , - 1 ,  0 , -1],\
		[0 ,  0 , - 1 , - 1 ,  0 ,  0 ,  1 , - 1 , -2],\
		[0 ,  0 ,  1 ,  0 ,  0 , - 1 ,  0 , - 1 , -1],\
		[1 ,  0 ,  0 ,  0 , - 1 ,  0 , - 1 ,  0 , -1],\
		[-1 , - 1 , - 1 ,  0 ,  0 ,  1 ,  0 ,  1 , -2],\
		[0 , - 1 , - 1 ,  0 ,  1 ,  0 ,  1 ,  1 , -1],\
		[-1 , - 1 ,  0 ,  0 ,  1 ,  1 ,  0 , - 1 , -2],\
		[-1 ,  1 , - 1 ,  0 ,  0 ,  0 ,  0 , - 1 , -2],\
		[1 ,  0 ,  0 ,  0 ,  0 , - 1 ,  0 , - 1 , -1],\
		[0 ,  0 ,  0 ,  1 ,  0 , - 1 , - 1 , - 1 , -2],\
		[-1 ,  0 ,  0 , - 1 ,  0 ,  1 ,  0 , - 1 , -2],\
		[0 ,  0 ,  0 , - 1 ,  0 , - 1 , - 1 ,  1 , -2]]
	NUMBER = 9
	model = "slim.lp"
	fileobj = open(model, "a")
	for k in range(0,4):
		for coff in S_T:
			temp = []
			for u in range(0,4):
				temp.append(str(coff[u]) + " " + "sx" + str((k * 4) + u) + "_" + str(n))
			for v in range(0,4):
				temp.append(str(coff[v + 4]) + " " + "sy" + str((k * 4) + v) + "_" + str(n))
			temp1 = " + ".join(temp)
			temp1 = temp1.replace("+ -", "- ")
			s = str(coff[NUMBER - 1])
			s = s.replace("--", "")
			temp1 += " >= " + s
			fileobj.write(temp1)
			fileobj.write("\n")
	fileobj.close(); 

def Variables(n):
	"""--------------------------
	Generate variables.
	--------------------------"""	
	model = "slim.lp"
	fileobj = open(model, "a")
	
	variable = []
	
	"""--------------------------
	Generate variables for slim.
	--------------------------"""
	# 1st - nth round variables
	for i in range(32):
		fileobj.write("x" + str(i) + "_" + str(n))
		fileobj.write("\n")
	for i in range(16):
		fileobj.write("sx" + str(i) + "_" + str(n))
		fileobj.write("\n")
	for i in range(16):
		fileobj.write("sy" + str(i) + "_" + str(n))
		fileobj.write("\n")

	for i in range(len(variable)):
		var = variable[i]
		fileobj.write(str(var)) 
		fileobj.write("\n")
	fileobj.close()
	return variable