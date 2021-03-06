from constants import *
import copy

class LOG():

	def __init__(self, csp, asmnt, confset):
		self.csp = csp
		self.asmnt = asmnt
		self.confset = confset
		self.s_counter = 0
		self.f_solutions = open("solutions.log", "w")
		self.f_contradictions = open("contradictions.log", "w")
	
	def format_solution(self, a):
		formatted = ""
		for i in range(1, 8):
			formatted += "Node "+str(i)+" ("
			formatted += "D=" + str(a["D"+str(i)]) + ", "
			formatted += "TH=" + str(a["TH"+str(i)]) + ", "
			formatted += "R=" + str(a["R"+str(i)]) + ", "
			formatted += "L=" + str(a["L"+str(i)]) + ""
			formatted += ")\n"
		return formatted
	
	def solution(self, stats):
		self.s_counter += 1
		print(self.s_counter)
		formatted = self.format_solution(self.asmnt.assignment)
		msg = "\n" + str(self.s_counter)
		msg += "\n\n" + formatted
		msg += "\n"
		for key, val in stats.items():
			msg += str(val) + " : " + key + "\n"
			stats[key] = 0
		print(msg, file=self.f_solutions)
		
	def contradiction(self, _type, res, curvar, value):
		msg = "\n" + res[2] + "(" + ",".join(res[1]) + ")"
		varvals = []
		for v in res[1]:
			varvals.append(v+"="+str(self.asmnt.assignment[v]))
		msg += "  {" + ",".join(varvals)+"}"
		msg += "  " + _type
		msg += "  " + curvar + ": " + str(value)
		msg += "  "+",".join(self.asmnt.assigned)
		print(msg, file=self.f_contradictions)
