from constants import *
import math

class HALF():
	'''Implements consistency algorithm for the half constraint.
	
        The second node must be double the length of the first node. i.e. :

        L1 = L2 / 2     or      L2 = L1 * 2
				
		This algorithm also handles propagation. That is, when L1 or L2 are
		reduced by other constraints, the effect is kept in check.

		If L1 is reduced, the boundary of both L1 and L2 are examined and made
		consistent. If this reduction makes consistency impossible,
		contradiction is reported.'''
	
	def establish(self, csp, curvar, value, participants, kook):
		'''Establishes consistency after assignment curvar: value.
		
		The domain of L2 reduces to L1 * 2. Or, the domain of L1 reduces to
		L2 / 2.
	
		After consistency, L2 or L1 reduces to one value only; however, its
		domain is now represented via bounds with equal min & max.'''
		A = csp.get_assignment()
		D = csp.get_domains()
		L1, L2 = sorted(participants) # L1 could be L1, L8, L15, and so on
		if L1 in A and L2 in A:
			return REVISED_NONE
		if curvar == L1: # L2 is not assigned
			new_value = value * 2
			if new_value < D[L2]["min"] or new_value > D[L2]["max"]:
				return (CONTRADICTION, {L2})
			if D[L2]["min"] == D[L2]["max"]:
				return ALREADY_CONSISTENT
			else:
				csp.update_domain(L2, {"min": new_value, "max": new_value})
				return (MADE_CONSISTENT, {L2})
		else: # L1 is not assigned
			new_value = math.ceil(value / 2)
			if new_value < D[L1]["min"] or new_value > D[L1]["max"]:
				return (CONTRADICTION, {L1})
			if D[L1]["min"] == D[L1]["max"]:
				return ALREADY_CONSISTENT
			else:
				csp.update_domain(L1, {"min": new_value, "max": new_value})
				return (MADE_CONSISTENT, {L1})

	def propagate(self, csp, reduced_vars, participants, kook):
		'''Establishes consistency when L1 andor L2 are reduced elsewhere.
		
		If contradiction occurs, both L1 and L2 are deemed failed.
		We cannot return one of them since their domains fail together.

		Take the following case:

		"L1": {"min": 20, "max": 20}
		"L2": {"min": 41, "max": 70}
		
		This contradiction occurs since ALL tuples of values for L1 and L2
		together violate the half constraint.
		
		Therefore, in all constraint we shall deem ALL unassigned participants
		failed.'''
		A = csp.get_assignment()
		L1, L2 = sorted(participants) # L1 could be L1, L8, L15, and so on
		if L1 in A or L2 in A:	# Already made consistent by establish
			return REVISED_NONE
		D = csp.get_domains()
		reduced = set([])
		(low1, up1) = self.__revise_L1(D, L1, L2)
		(low2, up2) = self.__revise_L2(D, L1, L2)
		if self.___consistent(low1, up1, low2, up2):
			return ALREADY_CONSISTENT
		if self.__contradiction(low1, up1, low2, up2):
			return (CONTRADICTION, {L1, L2})
		(low1, up1, low2, up2) = self.__mix(D, low1, up1, low2, up2, L1, L2)
		if up1 - low1 < D[L1]["max"] - D[L1]["min"]:
			reduced.add(L1)
			csp.update_domain(L1, {"min": low1, "max": up1})
		if up2 - low2 < D[L2]["max"] - D[L2]["min"]:
			reduced.add(L2)
			csp.update_domain(L2, {"min": low2, "max": up2})
		if len(reduced) == 0:
			return ALREADY_CONSISTENT
		return (MADE_CONSISTENT, reduced)
	
	def __mix(self, D, low1, up1, low2, up2, L1, L2):
		if low1 in (DOMAIN_INTACT, CONTRADICTION):
			low1 = D[L1]["min"]
		if up1 in (DOMAIN_INTACT, CONTRADICTION):
			up1 = D[L1]["max"]
		if low2 in (DOMAIN_INTACT, CONTRADICTION):
			low2 = D[L2]["min"]
		if up2 in (DOMAIN_INTACT, CONTRADICTION):
			up2 = D[L2]["max"]
		return (low1, up1, low2, up2)		

	def __contradiction(self, low1, up1, low2, up2):
		if low1 == CONTRADICTION and up1 == CONTRADICTION:
			if low2 == CONTRADICTION and up2 == CONTRADICTION:
				return True
		return False

	def ___consistent(self, low1, up1, low2, up2):
		if low1 == DOMAIN_INTACT and up1 == DOMAIN_INTACT:
			if low2 == DOMAIN_INTACT and up2 == DOMAIN_INTACT:
				return True
		return False

	def __revise_L1(self, D, L1, L2):
		low = math.ceil(D[L2]["min"] / 2)
		if low == D[L1]["min"]:
			low = DOMAIN_INTACT
		elif low < D[L1]["min"] or low > D[L1]["max"]:
			low = CONTRADICTION
		up = math.ceil(D[L2]["max"] / 2)
		if up == D[L1]["max"]:
			up = DOMAIN_INTACT
		elif up < D[L1]["min"] or up > D[L1]["max"]:
			up = CONTRADICTION
		return (low, up)
		
	def __revise_L2(self, D, L1, L2):
		low = D[L1]["min"] * 2
		if low == D[L2]["min"]:
			low = DOMAIN_INTACT
		elif low < D[L2]["min"] or low > D[L2]["max"]:
			low = CONTRADICTION
		up = D[L1]["max"] * 2
		if up == D[L2]["max"]:
			up = DOMAIN_INTACT
		elif up < D[L2]["min"] or up > D[L2]["max"]:
			up = CONTRADICTION
		return (low, up)
