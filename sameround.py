from constants import *

class SAMEROUND():
	'''Applies same roundness constraints.'''

	def __init__(self, csp):
		self.__csp = csp
	
	def b_update(self, reduced_vars):
		'''Establishes indirect consistency W.R.T. same_r.
		
		Since R1 is selected first, the rest of R variables 
		are already consistent.'''
		return (DOMAINS_INTACT, set([]))
	
	def __has_impact(self, curvar):
		'''Decides whether assignment to curvar could impact others.'''
		return curvar != "R1"
	
	def __new_domains(self, curvar, value, D):
		'''Returns new domains for participating variables.
		
		This is a mathematical function.'''
		newdomains = {}
		if curvar == "R1":
			impacted = {"R2", "R3", "R4", "R5", "R6", "R7"}
		for _var in impacted.copy():
			if not value in D[_var]:
				return CONTRADICTION
			elif len(D[_var]) == 1:
				continue
			newdomains[_var] = {value}
		return newdomains
			 
	def establish(self, curvar, value):
		'''Establishes consistency W.R.T. same_r constraint.'''
		if not self.__has_impact(curvar):
			return (DOMAINS_INTACT, set([]))
		D = self.csp.get_domains()
		newdomains = self.__new_domains(curvar, value, D)
		if newdomains == CONTRADICTION:
			return (CONTRADICTION, set([]), "same_r")
		impacted = set(newdomains.keys())
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		for vi, new_domain in newdomains.items():
			self.csp.update_d(vi, new_domain)
		return (DOMAINS_REDUCED, impacted)
