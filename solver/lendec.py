from constants import *
import math

class LENDEC():
	'''Applies length decrement consistency.
	
	The following relations must hold between L2 through L7:
	
		L2 > L3 > 2/3 L2
		L3 > L4 > 2/3 L3
		L4 > L5 > 2/3 L4
		L5 > L6 > 2/3 L5
		L6 > L7
	
	TODO: Move the following descriptions into the paper.

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

	def __init__(self, csp):
		self.__csp = csp
	
	def __getprevs(self, A, D, start_var):
		if start_var in A:
			lprev = A[start_var]["min"]
			uprev = A[start_var]["max"]
		else:
			lprev = D[start_var]["min"]
			uprev = D[start_var]["max"]
		return (lprev, uprev)
	
	def __newbounds(self, A, D, start_var):
		'''Returns new consistent bounds W.R.T. length decrement.
	
		This is a mathematical function.'''
		(lprev, uprev) = self.__getprevs(A, D, start_var)
		start_i = self.var_i(start_var)
		newbounds = {}		
		for i in range(start_i + 1, 8):
			li = "L" + str(i)
			lower = D[li]["min"]
			if i < 7:
				lower = max(D[Li]["min"], math.ceil(2/3 * lprev))
			upper = min(D[Li]["max"], uprev - 1)
			if lower < D[li]["min"] or lower > D[li]["max"]:
				return CONTRADICTION
			if upper < D[li]["min"] or upper > D[li]["max"]:
				return CONTRADICTION	
			if lower == D[li]["min"] and upper == D[li]["max"]:
				break
			newbounds[li] = {"min": lower, "max": upper}
			lprev = lower
			uprev = upper
		return newbounds
					
	def __establish(self, start_var):
		'''Establishes both indirect and direct l_dec consistency.
	
		lower3 = max(lower3, 2/3 lower2)
		upper3 = min(upper3, upper2 - 1)

		lower4 = max(lower4, 2/3 lower3)
		upper4 = min(upper4, upper3 - 1)

		lower5 = max(lower5, 2/3 lower4)
		upper5 = min(upper5, upper4 - 1)

		lower6 = max(lower6, 2/3 lower5)
		upper6 = min(upper6, upper5 - 1)
		
		upper7 = min(upper7, upper6 - 1)
		
		This is a mutable shell function.'''
		A = self.csp.get_assignment()
		D = self.csp.get_domains()
		newbounds = self.__newbounds(A, D, start_var)
		if newbounds == CONTRADICTION:
			return (CONTRADICTION, set([]), "l_dec")
		impacted = set(newbounds.keys())
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		for Li, new_domain in newbounds.items():
			self.csp.update_d(Li, new_domain)
		return (DOMAINS_REDUCED, impacted)
		
	def b_update(self, reduced_vars):
		'''Establishes indirect consistency W.R.T. l_dec constraint.
		
		if, say, L4, L5, and L6 are reduced, establishing consistency
		just for L4 makes consistency of L5 and L6 fall into place.'''
		reduced_sorted = sorted(reduced_vars)
		start_var = reduced_sorted[0]
		return self.__establish(start_var)

	def __has_impact(self, curvar):
		return curvar != "L7"
		
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
		lower6 = max(lower6, 2/3 lower5)'''
		if not self.__has_impact(curvar):
			return (DOMAINS_INTACT, None)
		return self.__establish(curvar)
