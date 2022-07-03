from constants import *
import copy

class LOG():

	def __init__(self):
		self.f = open("log.log", "w")
	
	def log1(self, curvar, value, cs, asmnt):
		msg = "Establishing " + curvar + " : " + str(value) + "\n\n"
		_assignments = ""
		for v in asmnt.assigned:
			_assignments += "    "+v+" : "+str(asmnt.assignment[v]) + "\n"
		msg += "  Assignments => \n\n" + _assignments + "\n\n"
		msg += "  Constraints => " + str(cs) + "\n\n"
		print(msg, file=self.f)
	
	def log2(self, dback, d, c, eresult):
		msg = "    Applied " + c + " => " + eresult[0]
		if eresult[0] == DOMAINS_REDUCED:
			msg += "\n"
			msg += self.add_domain_diff(dback, d, eresult[1])
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
	
	
	def log3(self, dback, d, _vars, bresult):
		msg = "     Bounds updated for " + str(sorted(_vars)) 
		msg += " => " + bresult[0] + "\n\n"
		if bresult[0] == DOMAINS_REDUCED:
			msg += self.add_domain_diff(dback, d, bresult[1])
		print(msg, file=self.f)
			
	def log4(self, curvar, jump_target):
		msg = "Jumped over "+curvar+"   -   target -> "+jump_target+"\n"
		print(msg, file=self.f)
		
	def log5(self, curvar):
		msg = "Jumped to "+curvar+"\n"
		print(msg, file=self.f)

	def log6(self, curvar):
		print(curvar+" exhausted.\n", file=self.f)

logger = LOG()
