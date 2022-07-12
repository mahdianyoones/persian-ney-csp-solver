from constants import *
import os
import copy

class LOG():

	def __init__(self, csp, asmnt, confset):
		self.csp = csp
		self.asmnt = asmnt
		self.confset = confset
		self.cstats = {"vars": {}, "consts": {}, 
			"direct": 0, "indirect": 0}
		for v in csp.X:
			self.cstats["vars"][v] = 0
		for c in csp.C.keys():
			self.cstats["consts"][c] = 0
		self.c_counter = 0
		self.f_solutions = open("solutions.log", "a")
		self.f_contradictions = open("contradictions.log", "a")
	
	def format_solution(self, a):
		formatted = "\n"
		for i in range(1, 8):
			formatted += "Node "+str(i)+" ("
			formatted += "D=" + str(a["D"+str(i)]) + ", "
			formatted += "TH=" + str(a["TH"+str(i)]) + ", "
			formatted += "R=" + str(a["R"+str(i)]) + ", "
			formatted += "L=" + str(a["L"+str(i)]) + ""
			formatted += ")\n"
		return formatted
	
	def solution(self, stats, cook, spec):
		print(cook, " : ", "\n")
		formatted = self.format_solution(self.asmnt.assignment)
		print(spec, "\n")
		msg += "\n\n" + formatted
		msg += "\n"
		for key, val in stats.items():
			msg += str(val) + " : " + key + "\n"
			stats[key] = 0
		print(msg, file=self.f_solutions)
	
	def format_cont_stats(self):
		msg = "Direct = " + str(self.cstats["direct"]) + "  "
		msg += "Indirect = " + str(self.cstats["indirect"]) + "\n\n"
		consts = []
		for c, cvalue in self.cstats["consts"].items():
			consts.append(c + " = " + str(cvalue))
		_vars = {"Ds": [], "THs": [], "Rs": [], "Ls": []}
		for v, vvalue in self.cstats["vars"].items():
			if v[0] == "L":
				_vars["Ls"].append(v + " = " + str(vvalue))
			elif v[0] == "D":
				_vars["Ds"].append(v + " = " + str(vvalue))
			elif v[0] == "R":
				_vars["Rs"].append(v + " = " + str(vvalue))
			else:
				_vars["THs"].append(v + " = " + str(vvalue))
		msg += "Constraints: \n\n" + "  ".join(consts)
		msg += "\n\nVariables: \n\n"
		msg += "  ".join(_vars["Ls"]) + "\n\n"
		msg += "  ".join(_vars["Ds"]) + "\n\n"
		msg += "  ".join(_vars["Rs"]) + "\n\n"
		msg += "  ".join(_vars["THs"]) + "\n\n"
		msg += "Assigned: " + "  ".join(self.asmnt.assigned)
		return msg
		
	def contradiction(self, _type, res, curvar, value):
		self.c_counter += 1
		self.cstats["vars"][curvar] += 1
		self.cstats["consts"][res[2]] += 1
		self.cstats[_type] += 1
		if self.c_counter % 100 == 0:
			os.system("clear")
			print(self.format_cont_stats())
			#print(msg, file=self.f_contradictions)
