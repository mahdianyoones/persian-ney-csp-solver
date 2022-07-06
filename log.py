from constants import *
import copy

class LOG():

	def __init__(self):
		self.f = open("log.log", "w")
	
	def log2(self, curvar, value, asmnt):
		msg = "\n"
		msg += "    Assigned " + curvar + " : " + str(value) + "\n\n"
		for v in asmnt.assigned:
			msg += "        " + v + " : " + str(asmnt.assignment[v])
			msg += "\n"
		print(msg, file=self.f)
	
	def log1(self, dback, d, var, val, dir_res):
		msg = ""
		msg += "Established " + var + " : " + str(val)
		msg += " => " + dir_res[0]
		if dir_res[0] == CONTRADICTION:
			msg += "  due to  " + dir_res[2] + "\n"
		#elif dir_res[0] == DOMAINS_REDUCED:
			#msg += "\n\n"
			#msg += self.add_domain_diff(dback, d, dir_res[1])
		#else:
		print(msg, file=self.f)			
	
	def add_domain_diff(self, dback, d, _vars):
		msg = ""
		for v in sorted(_vars):
			if v[0] == "L":
				b = before = dback[v]
				a = after = d[v]
				lenafter = (a["max"]-a["min"])+1
				diff = str((b["max"]-b["min"])-(a["max"]-a["min"]))
			else:
				before = dback[v]
				after = d[v]
				diff = len(before) - len(after)
				lenafter = len(after)
			msg += "      "+v+" ----> shed " + str(diff) + ","
			msg += "    "+str(lenafter)+" are left.\n"
#			msg += "        before => " + str(before) + "\n\n"
#			msg += "        after => " + str(after) + "\n\n"
		return msg
	
	
	def log3(self, dback, d, _vars, indir_res):
		msg = "\n"
		msg += "    Bounds updated for " + str(sorted(_vars))
		msg += "  =>  "+ indir_res[0]
		if indir_res[0] == CONTRADICTION:
			msg += "\n              due to  " + indir_res[2]
			msg += ", cs :  " + str(indir_res[1]) + "\n\n"
		#elif indir_res[0] == DOMAINS_REDUCED:
		#	msg += self.add_domain_diff(dback, d, indir_res[1])
		print(msg, file=self.f)
			
	def log4(self, curvar, jump_target):
		msg = "\n\n"
		msg += "Jumped over " + curvar
		msg += "  target -> " + jump_target
		print(msg, file=self.f)
		
	def log5(self, curvar):
		msg = "\n\n"
		msg += "Jumped to " + curvar
		print(msg, file=self.f)

	def log6(self, curvar):
		msg = "\n\n"
		msg += curvar + " exhausted."
		print(msg, file=self.f)

logger = LOG()
