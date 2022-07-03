from holes import HOLES
from len import LEN
from l_dec import L_DEC
from d_dec import D_DEC
from same_thr import SAME_THR
from l1_half_l2 import L1_HALF_L2
from in_stock import IN_STOCK
from constants import *
from log import logger
import copy

class MAC():
	'''Implements MAC through special consistency algorithms.
				
	Impacts due to {D1: 18}: 
	
	<<Direct>>
	
		D1 ---------------------> R1, TH1, L1
		      due to in_stock

		D1 ---------------------> D2, D3, D4, D5, D6, D7
		       due to d_dec
	
	<<Indirect>>
	
		L1 ----------------------> L2 
	          due to l1_half_l2
	          
	     L1 -----------------------------------------> a subset of {L2, L3, L4, L5}
	     	  due to h1, h2, h3, h4, h5, and h6 

		R1 ---------------------> R2, R3, R4, R5, R6, R7
	     	  due to same_r
	        
		TH1 ---------------------> TH2, TH3, TH4, TH5, TH6, TH7
			  due to same_th
	
	Impacts due to {D1: 18, TH1: 2}: (TH1 is assigned after D1)
	
	<<Direct>>
	
		TH1 ---------------------> R1, L1
		      due to in_stock

		TH1 ---------------------> TH2, TH3, TH4, TH5, TH6, TH7
		       due to same_th
		       
	<<Indirect>>
	
		L1 ----------------------> L2
	          due to l1_half_l2
	          
	     L1 -----------------------------------------> a subset of {L2, L3, L4, L5}
	     	due to h1, h2, h3, h4, h5, and h6 

		R1 ---------------------> R2, R3, R4, R5, R6, R7
	     	  due to same_r
	     	  
	Impacts due to {D2: 17}

	<<Direct>>
	
		D2 ---------------------> R2, TH2, L2
		      due to in_stock

		D2 ---------------------> D3, D4, D5, D6, D7
		       due to d_dec
	
	<<Indirect>>
	
		L2 --------------------------> L3, L4, L5, L6, L7
	             due to l1_half_l2

	     L2 -----------------------------------------> a subset of {L1, L3, L4, L5}
	     	due to h1, h2, h3, h4, h5, and h6 

		R2 ------------------------> R3, R4, R5, R6, R7
	     	     due to same_r
	        
		TH2 -------------------------> TH3, TH4, TH5, TH6, TH7
			    due to same_th


	'''
	def __init__(self, csp):
		self.csp = csp
		self.neighbors = {}
		self.in_stock = IN_STOCK(csp)
		self.holes = HOLES(csp)
		self.len = LEN(csp)
		self.d_dec = D_DEC(csp)
		self.l_dec = L_DEC(csp)
		self.same_thr = SAME_THR(csp)
		self.l1_half_l2 = L1_HALF_L2(csp)
		self.alg_ref = {
			"h1":		self.holes,
			"h2":		self.holes,
			"h3":		self.holes,
			"h4":		self.holes,
			"h5":		self.holes,
			"h6":		self.holes,
			"l1_half_l2":	self.l1_half_l2,
			"in_stock": 	self.in_stock,
			"same_th":	self.same_thr,
			"same_r":		self.same_thr,
			"l_dec":		self.l_dec,
			"d_dec":		self.d_dec,
			"len":		self.len
		}

	def neighborhood(self, curvar):
		'''Returns variables that share a constraint with curvar.
		
		Returns a dictionary of this format:
		{
			"constraint 1": {a set of neighbors connected via constraint 1},
			"constraint 2": {a set of neighbors connected via constraint 2},
			...
		}
		
		To boost performace, neighbors are cached in self.neighbors.
		'''
		if not curvar in self.neighbors:
			self.neighbors[curvar] = {}
			for constraint, _vars in self.csp.C.items():
				if curvar in _vars:
					self.neighbors[curvar][constraint] = _vars
		return self.neighbors[curvar]
	
	def b_update(self, asmnt, _vars=set([])):
		if len(_vars) == 0:
			constraints = set(self.csp.C.keys())
		else:
			constraints = set([])
			for _var in _vars:
				neighborhood = self.neighborhood(_var)
				constraints.update(set(neighborhood.keys()))
		impacted = set([])
		while len(constraints) > 0:
			c = constraints.pop()
			bresult = self.alg_ref[c].b_update(asmnt)
			if bresult[0] == CONTRADICTION:
				return bresult
			if bresult[0] == DOMAINS_REDUCED:
				impacted.update(bresult[1])
				for rvar in bresult[1]:
					neighborhood = self.neighborhood(rvar)
					impacted_cs = neighborhood.keys()
					constraints.update(set(impacted_cs))
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		return (DOMAINS_REDUCED, impacted)
		
	def establish(self, asmnt, curvar, value):
		'''Establishes consistency for curvar neighbors and returns a conflict set.
		
		If the domain of a neighbor changes, neighbors of that neighbor are also
		checked for reduction.
		
		curvar is the variable which neighbors are to be made consistent.
		Before search, bounds on varaibles needs to be made consistent.
		Therefore, this method is called for all variables one by one with
		value = None. 
		
		Individual consistency algorithms (i.e. other methods of this class),
		detect if there is an oppotunity to reduce the domain of variables
		W.R.T. curvar.
		'''
		neighborhood = self.neighborhood(curvar)
		cs = set(neighborhood.keys())
		logger.log1(curvar, value, cs, asmnt)
		impacted = set([])
		for c in cs:
			dback = copy.deepcopy(self.csp.D)
			eresult = self.alg_ref[c].establish(asmnt, curvar, value)
			logger.log2(dback, self.csp.D, c, eresult)
			if eresult[0] == DOMAINS_REDUCED:	
				impacted.update(eresult[1])
				dback = copy.deepcopy(self.csp.D)
				bresult = self.b_update(asmnt, eresult[1])
				if bresult[0] == CONTRADICTION:
					return bresult
				if bresult[0] == DOMAINS_REDUCED:
					impacted.update(bresult[1])
				logger.log3(dback, self.csp.D, eresult[1], bresult)
			elif eresult[0] == CONTRADICTION:
				return eresult
		if len(impacted) == 0:
			return (DOMAINS_INTACT, set([]))
		return (DOMAINS_REDUCED, impacted)
