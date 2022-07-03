from constants import *

class LOG():

	def __init__(self):
		self.f = open("log.log", "w")
	
	def log1(self, curvar, value, cs, asmnt):
		msg = "Establishing " + curvar + " : " + str(value) + "\n\n"
		msg += "  Assignments => " + str(asmnt.assignment) + "\n\n"
		msg += "  Constraints => " + str(cs) + "\n\n"
		print(msg, file=self.f)
	
	def log2(self, dback, d, c, eresult):
		msg = "    Applied " + c + " => " + eresult[0] + "\n\n"
		if eresult[0] == DOMAINS_REDUCED:
			msg += self.add_domain_diff(dback, d, eresult[1])
		print(msg, file=self.f)			
	
	def add_domain_diff(self, dback, d, _vars):
		msg = ""
		for v in _vars:
			if v[0] == "L":
				b = before = dback[v]
				a = after = d[v]
				diff = str((b["max"]-b["min"])-(a["max"]-a["min"]))
			else:
				before = set(sorted(dback[v]))
				after = set(sorted(d[v]))
				diff = len(before) - len(after)
			msg += "      "+v+" ----> shed " + str(diff) + " values. \n\n"
#			msg += "        before => " + str(before) + "\n\n"
#			msg += "        after => " + str(after) + "\n\n"
		return msg
	
	
	def log3(self, dback, d, _vars, bresult):
		msg = "     Bounds updated for " + str(sorted(_vars)) 
		msg += " => " + bresult[0] + "\n\n"
		if bresult[0] == DOMAINS_REDUCED:
			msg += self.add_domain_diff(dback, d, bresult[1])
		print(msg, file=self.f)
			
logger = LOG()
