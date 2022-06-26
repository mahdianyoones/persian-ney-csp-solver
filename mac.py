from holes import HOLES
from len import LEN
from l_dec import L_DEC
from d_dec import D_DEC
from same_thr import SAME_THR
from l1_half_l2 import L1_HALF_L2
from in_stock import IN_STOCK
from constants import *

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
			"h1":		self.holes.establish,
			"h2":		self.holes.establish,
			"h3":		self.holes.establish,
			"h4":		self.holes.establish,
			"h5":		self.holes.establish,
			"h6":		self.holes.establish,
			"l1_half_l2":	self.l1_half_l2.establish,
			"in_stock": 	self.in_stock.establish,
			"same_th":	self.same_thr.establish,
			"same_r":		self.same_thr.establish,
			"l_dec":		self.l_dec.establish,
			"d_dec":		self.d_dec.establish,
			"len":		self.len.establish
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
		reduced = set([curvar])
		self.csp.backup_d()
		while len(reduced) > 0:
			curvar = reduced.pop()
			neighborhood = self.neighborhood(curvar)
			my_cs = neighborhood.keys()
			for c in my_cs:
				cresult = self.alg_ref[c](asmnt, curvar, value)
				if cresult[0] == CONTRADICTION:
					self.csp.revert_d()
					return (FAILURE, cresult[1])
				elif cresult[0] == DOMAINS_INTACT:
					continue
				elif cresult[0] == DOMAINS_REDUCED:
					reduced.update(cresult[1])
		# All domains have survived consistency.
		return (SUCCESS, None)
