from constants import *
import math
from base import BASE

class L_DEC(BASE):
	'''Applies length decrement consistency.
	
	The following relations must hold between L2 through L7:
	
		L2 > L3 > 2/3 L2
		L3 > L4 > 2/3 L3
		L4 > L5 > 2/3 L4
		L5 > L6 > 2/3 L5
		L6 > L7'''

	#TODO: Move the following descriptions into the paper.
	'''
	This consistency function is called on two occasions:
		1- An L variable is assigned a value
		2- Domain of an L variable has been reduced
		
		In case 1, we use the assigned value to determine a new 
		consistent range for further variables. For example, if L3 
		is assigned, say, 100, upper bound on L4, L5, L6 reduce to 
		99, 98, 97, and 96 respectively. Furthermore, the lower bounds
		of L4, L5, and L6 reduce to around 66, 44, and 29 respectively.
		i.e. {L3: 100} propagates to
		
			L4 -> [66, 99] 
			L5 -> [44, 98]
			L6 -> [29, 96]
		
		In case 2, we use new bounds on the variable whose domain has
		been reduced. That variable is curvar. For example, if the 
		domain of L3 has reduced to, say, [80, 120], the domain of 
		L4, L5, and L6 change as such:
		
			L4 -> [53, 119]
			L5 -> [35, 118]
			L6 -> [23, 117]
		
		From the two examples above, we can observe that assigning
		values to variables can trigger stronger domain reduction
		in propagation.
	'''

	def __init__(self, csp, asmnt):
		self.csp = csp
		self.asmnt = asmnt
	
	def _establish(self, start_var):
	'''Establishes both indirect and direct l_dec consistency.
	
		lower3 = max(lower3, 2/3 lower2)
		upper3 = min(upper3, upper2 - 1)

		lower4 = max(lower4, 2/3 lower3)
		upper4 = min(upper4, upper3 - 1)

		lower5 = max(lower5, 2/3 lower4)
		upper5 = min(upper5, upper4 - 1)

		lower6 = max(lower6, 2/3 lower5)
		upper6 = min(upper6, upper5 - 1)
		
		upper7 = min(upper7, upper6 - 1)'''
		
		impacted = set([])
		contradiction = False
		start_i = self.var_i(start_var)
		asmnt = self.asmnt.assignment
		if start_var in self.asmnt.assigned:
			lower_prev = asmnt[start_var]["min"]
			upper_prev = asmnt[start_var]["max"]
		else:
			lower_prev = self.csp.D[start_var]["min"]
			upper_prev =  = self.csp.D[start_var]["max"]
		for i in range(start_i+1, 8):
			li = "L"+str(i)
			di = self.csp.D[li]
			if i < 7:				
				loweri = max(di["min"], math.ceil(2/3 * dprev["min"]))
				if loweri < di["min"] or loweri > di["max"]:
					contradiction = True
					break
				if loweri > di["min"]:
					self.csp.D[li]["min"] = loweri
					impacted.add(li)
					lower_prev = loweri
				else:
					break
			upperi = min(di["max"], upper_prev - 1)
			if upperi < di["min"] or upperi > di["max"]:
				contradiction = True
				break
			if upperi < di["max"]:
				self.csp.D[li]["max"] = upperi
				impacted.add(li)
				upper_prev = upperi
			elif not li in impacted: # its lower bound might have changed
				break
		return (contradiction, impacted)
		
	def b_update(self, reduced_vars):
	'''Establishes indirect consistency W.R.T. l_dec constraint.
	
	if, say, L4, L5, and L6 are reduced, establishing consistency for L4 only
	makes L5 and L6 consistency also fall into place.'''
		reduced_sorted = sorted(reduced_vars)
		(contradiction, impacted) self._establish(reduced_sorted[0])
		if contradiction:
			return (CONTRADICTION, set([]), "l_dec")
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))		

	def establish(self, curvar, value):
	'''Establishes direct consistency W.R.T. l_dec constraint.
	
		upper3 = min(upper3, L2 - 1)
		upper4 = min(upper4, upper3 - 1)
		upper5 = min(upper5, upper4 - 1)
		upper6 = min(upper6, upper5 - 1)
		upper7 = min(upper7, upper6 - 1)
		
		lower3 = max(lower3, 2/3 * L2)
		lower4 = max(lower4, 2/3 lower3)
		lower5 = max(lower5, 2/3 lower4)
		lower6 = max(lower6, 2/3 lower5)	
	'''
		if curvar == "L7":
			return (DOMAINS_INTACT, None)
		(contradiction, impacted) = self._establish(curvar)
		if contradiction:
			return (CONTRADICTION, {curvar}, "l_dec")
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
