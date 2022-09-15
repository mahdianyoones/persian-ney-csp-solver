from constants import *
import copy

class DIAMDEC():
	'''Implements diameter decrement consistency.
	
	 0.5 <= D2 - D1 <= 1
	 0.5 <= D3 - D2 <= 1
	 0.5 <= D4 - D3 <= 1
	 0.5 <= D5 - D4 <= 1
	 0.5 <= D6 - D5 <= 1
	 0.5 <= D7 - D6 <= 1
	 
	 0.5 and 1 are subject to ney_spec.
	 
	 Inconsistent values can be removed from all D variables in one go.	 
	'''
	
	def __init__(self, csp):
		self.__csp = csp
		self.__ddiffmin = csp.spec["ddiff"]["min"]
	
	def __inconsistents(self, dall, ddiffmin, assignment):
		'''Returns inconsistent values of D1 to D7 W.R.T. d_dec.
		
		This is a mathematical function.'''
		incons = {}
		for i in range(1, 8):
			di = "D" + str(i)
			incons[di] = set([])
			if di in assignment:
				last_max = assignment[di]
				continue
			reduced = False
			for diameter in dall[di]:
				if diameter > last_max - ddiff_min:
					incons[di].add(diameter)
					reduced = True
			if not reduced:
				break
			if len(incons[di]) == len(dall[di]):
				break
			last_max = max(dall[di])
		return incons
	
	def __confset(self, incons, dall, assignment):
		'''Checks if a contradiction has occured and returns a conflit set.
		
		This is a mathematical function.'''
		confset = set([])
		contra = False
		for di, values in incons.items():
			if len(values) == len(dall[di]):
				contra = True
				break
			if di in assignment:
				confset.add(di)
		return (contra, confset)
	
	def __establish(self):
		'''Removes inconsistent values from all D variables W.R.T. d_dec.'''
		a = self.csp.get_assignment()
		incons = self.__inconsistents(self.csp.D, self.__ddiffmin, a)
		(contra, confset) = self.__confset(incons, self.csp.D. a)
		if contra:
			(True, confset, set([]))
		impacted = set([])
		for di, values in incons.items():
			if len(values) > 0:
				impacted.add(di)
				reduced_d = self.csp.D[di].difference(values)
				self.csp.update_d(di, reduced_d)
		return (False, set([]), impacted)
	
	def b_update(self):
		'''Establishes indirect d_dec consistency.'''
		(contr, confset, impacted) = self._establish()
		if contra:
			return (CONTRADICTION, set([]), "d_dec")
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
	
	def establish(self, curvar, value):
		'''Establishes direct d_dec consistency after assignment.
		
		e.g.
		
		If D1 and D2 are assigned and contradiction occurs for D5 (it runs 
		out of values), confset = {D1, D2}.
		
		We cannot tell whether other variables (Rs, Ths, and Ls) are
		responsible for this contradiction or not.
		'''
		(contra, confset, impacted) = self._establish()
		if contra:
			return (CONTRADICTION, confset, "d_dec")
		if len(impacted) > 0:
			(DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
