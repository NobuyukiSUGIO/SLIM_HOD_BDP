# -*- coding: utf-8 -*-
import time

from gurobipy import *

class Slim:
	def __init__(self, blocksize):
		self.blocksize = blocksize
		self.filename_result = "result.txt"
		
	def WriteObjective(self, obj):
		"""
		Write the objective value into filename_result.
		"""
		fileobj = open(self.filename_result, "a")
		fileobj.write("The objective value = %d\n" %obj.getValue())
		eqn1 = []
		eqn2 = []
		for i in range(0, self.blocksize):
			u = obj.getVar(i) 
			if u.getAttr("x") != 0:
				eqn1.append(u.getAttr('VarName'))
				eqn2.append(u.getAttr('x'))
		length = len(eqn1)
		for i in range(0,length):
			s = eqn1[i] + "=" + str(eqn2[i])
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()
		
	def SolveModel(self):
		"""
		Solve the MILP model to search the integral distinguisher.
		Grobi API
		https://www.gurobi.com/documentation/9.1/refman/py_python_api_details.html
		"""
		time_start = time.time()
		m = read("slim.lp")
		counter = 0
		set_zero = []
		global_flag = False
		while counter < self.blocksize:
			m.optimize() 
			# Gurobi syntax: m.Status == 2 represents the model is feasible.
			if m.Status == 2:
				obj = m.getObjective() # Retrieve the model objective(s).
				print("object value = ")
				print(obj.getValue())
				if obj.getValue() > 1:
					global_flag = True
					break
				else:
					fileobj = open(self.filename_result, "a")
					fileobj.write("************************************COUNTER = %d\n" % counter)
					fileobj.close()
					self.WriteObjective(obj)
					for i in range(0, self.blocksize):
						u = obj.getVar(i)
						temp = u.getAttr('x')
						if temp == 1:
							set_zero.append(u.getAttr('VarName'))
							u.ub = 0
							m.update()
							counter += 1
							break
			# Gurobi syntax: m.Status == 3 represents the model is infeasible.
			elif m.Status == 3:
				global_flag = True
				break
			else:
				print( "Unknown error!")

		fileobj = open(self.filename_result, "a")
		if global_flag:
			fileobj.write("\nIntegral Distinguisher Found!\n\n")
			print ("Integral Distinguisher Found!\n")
		else:
			fileobj.write("\nIntegral Distinguisher do NOT exist\n\n")
			print ("Integral Distinguisher do NOT exist\n")

		fileobj.write("Those are the coordinates set to zero: \n")
		for u in set_zero:
			fileobj.write(u)
			fileobj.write("\n")
		fileobj.write("\n")
		time_end = time.time()
		fileobj.write(("Time used = " + str(time_end - time_start) + "\n"))
		fileobj.close()