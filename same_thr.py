from constants import *
from base import BASE

class SAME_THR(BASE):
	'''Applies same thickness and roundness constraints.'''

	def __init__(self, csp, asmnt):
		self.__csp = csp
		self.__asmnt = asmnt
	
	def b_update(self, reduced_vars):
		'''Establishes indirect consistency W.R.T. same_th and same_r.
		
		Since TH1 and R1 are selected first, the rest of TH and R 
		variables are already consistent.'''
		return (DOMAINS_INTACT, set([]))
	
	def establish(self, curvar, value):
	'''Establishes consistency W.R.T. same_r and same_th constraints.'''
		if curvar != "TH1" or curvar != "R1":
			return (DOMAINS_INTACT, set([]))
		if curvar == "TH1":
			impacted = {"TH2", "TH3", "TH4", "TH5", "TH6", "TH7"}
		else:
			impacted = {"R2", "R3", "R4", "R5", "R6", "R7"}
		cname = "same_r" if curvar == "R1" else "same_th"
		for _var in impacted.copy():
			if not value in self.csp.D[_var]:
				return (CONTRADICTION, {curvar}, cname)
			if len(self.csp.D[_var]) == 1: # no change
				impacted.remove(_var)
				continue
			self.csp.D[_var] = {value}
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)	
		return (DOMAINS_INTACT, set([]))
