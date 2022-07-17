from constants import *
import copy
from base import BASE

class HOLES(BASE):
	'''Provides core consistency algorithm for h1, h2, h3, h4, h5, h6.
		
	All relations together:
	
	L1 + L2 + L3 + 10 			< h1
	L1 + L2 + L3 + 30 			< h2
	L1 + L2 + L3 + L4 + 10 		< h3
	L1 + L2 + L3 + L4 + 30 		< h4
	L1 + L2 + L3 + L4 + 50 		< h5
	L1 + L2 + L3 + L4 + L5 + 10 	< h6
	'''
	
	def __init__(self, csp, asmnt, h, space, p, o, plowers, cname):
		self.cname = cname
		self.csp = csp
		self.asmnt = asmnt
		self.h = h
		self.space = space
		self.participants = p
		self.others_map = o
		self.plowers = plowers

	def upper(self, *other_lows):
		return self.h - (sum(other_lows) + self.space)
		
	def lowers(self):
		lowers = {}
		for li in self.participants:
			if li in self.asmnt.assigned:
				lowers[li] = self.asmnt.assignment[li]
			else:
				lowers[li] = self.csp.D[li]["min"]
		return lowers
	
	def _establish(self):
		confset = set([])
		impacted = set([])
		contradiction = False
		a = self.asmnt.assigned
		lowers = self.lowers()
		for L in self.participants:
			if L in self.asmnt.assigned:
				continue
			other_lows = [lowers[otherL] for otherL in self.others_map[L]]
			upper = self.upper(other_lows)
			if upper < self.csp.D[L]["min"]
				confset = {v for v in pmap[L] if v in a}
				contradiction = True
				break
			elif upper < self.csp.D[L]["max"]:
				self.csp.D[L]["max"] = upper
				impacted.add(L)
		return (contradiction, confset, impacted)
	
		hmarg = spec["hmarg"]
		holed = self.csp.spec["holed"]
		self.spaces = [ None, hmarg * 1, hmarg * 2 + holed * 1, hmarg * 1, 
			hmarg * 2 + holed * 1, hmarg * 3 + holed * 2, hmarg * 1]
		self.holes = [None, spec["h1"], spec["h2"], spec["h3"], spec["h4"], 
			spec["h5"], spec["h6"]]
	
	def b_update(self, reduced_vars):
		'''Establishes indirect hole consistency on reduction of L vars.
		
		This indirect consistency for h1 constraint is triggered by updates
		on the lower bounds of L1, L2, and L3 according to the following:
		
		lower1 -> upper2, upper3
		lower2 -> upper1, upper3
		lower3 -> upper1, upper2
		
		and similarly for h2, h3, h4, h5, and h6
		'''
		triggered = False
		for reduced_var in reduced_vars:
			if reduced_var in self.participants:
				if self.plowers[p] < self.csp.D[p]["min"]:
					triggered = True
					break
		if triggered:
			(contradiction, confset, impacted) = self._establish()
			if contradiction:
				return (CONTRADICTION, set([]), self.cname)
			if len(impacted) > 0:
				for p in participants:
					self.plowers[p] = self.csp.D[p]["min"]
				return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
			
	def establish(self, curvar, value):
		'''Establishes direct hole consistency on assignment.

		From the relation of h1 constraint L1 + L2 + L3 + 10 < h1, 
		the following updates are done for upper bounds of L1, L2, and L3:
		
	 	upper1 = h1 - (lower2 + lower3 + 10)
		upper2 = h1 - (lower1 + lower3 + 10)
		upper3 = h1 - (lower1 + lower2 + 10)
		
		and similarly for h2, h3, h4, h5, and h6
		'''
		(contradiction, confset, impacted) = self._establish()
		if contradiction:
			return (CONTRADICTION, confset, self.cname)
		if len(impacted) > 0:
			(DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
