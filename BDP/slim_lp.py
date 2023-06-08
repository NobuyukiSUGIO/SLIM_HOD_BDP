# -*- coding: utf-8 -*-

from slim_functions import *

model = "slim.lp"
fileobj = open(model, "w")

"""--------------------------
Create object function
--------------------------"""	
fileobj.write("Minimize")
fileobj.write("\n")

# target round
R = 9

for i in range(32):
	if i != 31:
		fileobj.write("x"+ str(i) + "_" + str(R) + " + ")
	else:
		fileobj.write("x"+ str(i) + "_" + str(R))

fileobj.write("\n")

"""--------------------------
Create the constraints of SLIM
--------------------------"""	
fileobj.write("Subject To")
fileobj.write("\n")
fileobj.close()

for n in range(1, R+1):
	slim(n)
	for i in range(4):
		S(n)

"""--------------------------
Input Division Property
--------------------------"""	
model = "slim.lp"
fileobj = open(model, "a")

for i in range(32):
	if i == 16:
		fileobj.write("x"+ str(i) + "_0 = 0")
		fileobj.write("\n")
	else:
		fileobj.write("x"+ str(i) + "_0 = 1")
		fileobj.write("\n")

fileobj.write("Binary")
fileobj.write("\n")

# 0th round input variables
for i in range(32):
	fileobj.write("x" + str(i) + "_0")
	fileobj.write("\n")
fileobj.close()

# 1st,...,rth round variables
for i in range(1, R+1):
	Variables(i)
	
model = "slim.lp"
fileobj = open(model, "a")
fileobj.write("END")
fileobj.write("\n")
fileobj.close()