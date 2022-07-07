from constants import *
import copy

class LOG():

	def __init__(self, csp, asmnt):
		self.csp = csp
		self.asmnt = asmnt
		self.s_counter = 0
		self.f = open("log.log", "w")
	
	def log_solution(self, stats):
		self.s_counter += 1
		msg = "\n"+str(self.s_counter)+"\n\n"+str(self.asmnt.assignment)
		msg += "\n"
		for key, val in stats.items():
			msg += "\n"+key+" : "+str(val)
		print(msg, file=self.f)
