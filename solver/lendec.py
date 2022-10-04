from functools import reduce
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

		The assumption is that assignments occur in this order: L1, L2, L3,
		L4, L5, L6, and then L7.'''
	
	def establish(self, csp, curvar, value):
		'''Establishes consistency W.R.T. len decrement constraint.
	
		upper3 = min(upper3, L2 - 1)
		upper4 = min(upper4, upper3 - 1)
		upper5 = min(upper5, upper4 - 1)
		upper6 = min(upper6, upper5 - 1)
		upper7 = min(upper7, upper6 - 1)
		
		lower3 = max(lower3, 2/3 * L2)
		lower4 = max(lower4, 2/3 lower3)
		lower5 = max(lower5, 2/3 lower4)
		lower6 = max(lower6, 2/3 lower5)'''
		if curvar == "L7":
			return (DOMAINS_INTACT, set([]))
		return self.__establish(csp, curvar)

	def propagate(self, csp, reduced_vars):
		'''Establishes indirect consistency W.R.T. l_dec constraint.
		
		if, say, L4, L5, and L6 are reduced, establishing consistency
		just for L4 makes consistency of L5 and L6 fall into place.'''
		reduced_sorted = sorted(reduced_vars)
		start_var = reduced_sorted[0]
		return self.__establish(csp, start_var)

	def __establish(self, csp, start_var):
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
		A = csp.get_assignment()
		D = csp.get_domains()
		(newbounds, examined) = self.__newbounds(A, D, start_var)
		if newbounds == CONTRADICTION:
			return (CONTRADICTION, examined)
		for Li, new_domain in newbounds.items():
			csp.update_domain(Li, new_domain)
		reduced = set(newbounds.keys())
		if len(reduced) == 0:
			return (DOMAINS_INTACT, examined)
		return (DOMAINS_REDUCED, examined, reduced)

	def __getprevs(self, A, D, start_var):
		if start_var in A:
			lprev = A[start_var]
			uprev = A[start_var]
		else:
			lprev = D[start_var]["min"]
			uprev = D[start_var]["max"]
		return (lprev, uprev)
	
	def __in_range(self, range, value):
		return value >= range["min"] and value <= range["max"]
	
	def __reduced(self, upper, lower, domain):
		return upper - lower < domain["max"] - domain["min"]

	def __newbounds(self, A, D, start_var):
		'''Returns new consistent bounds W.R.T. length decrement.
	
		This is a mathematical function.'''
		(lprev, uprev) = self.__getprevs(A, D, start_var)
		newbounds = {}
		examined = set([])
		for i in range(int(start_var[1]) + 1, 8):
			li = "L" + str(i)
			examined.add(li)
			if i < 7:
				lower = math.ceil(2/3 * lprev)
			else:
				lower = min(D[li]["min"], lprev - 1)
			upper = uprev - 1
			if not self.__in_range(D[li], lower):
				return (CONTRADICTION, examined)
			if not self.__in_range(D[li], upper):
				return (CONTRADICTION, examined)
			if self.__reduced(upper, lower, D[li]):
				newbounds[li] = {"min": lower, "max": upper}
			lprev = lower
			uprev = upper
		return (newbounds, examined)