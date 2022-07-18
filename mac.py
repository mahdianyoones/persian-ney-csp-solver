from h1 import H1
from h2 import H2
from h3 import H3
from h4 import H4
from h5 import H5
from h6 import H6
from len import LEN
from l_dec import L_DEC
from d_dec import D_DEC
from same_thr import SAME_THR
from l1_half_l2 import L1_HALF_L2
from in_stock import IN_STOCK
from constants import *
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
	def __init__(self, csp, asmnt):
		self.csp = csp
		self.asmnt = asmnt
		self.neighbors = {}
		self.in_stock = IN_STOCK(csp, asmnt)
		self.h1 = H1(csp, asmnt)
		self.h2 = H2(csp, asmnt)
		self.h3 = H3(csp, asmnt)
		self.h4 = H4(csp, asmnt)
		self.h5 = H5(csp, asmnt)
		self.h6 = H6(csp, asmnt)
		self.len = LEN(csp, asmnt)
		self.d_dec = D_DEC(csp, asmnt)
		self.l_dec = L_DEC(csp, asmnt)
		self.same_thr = SAME_THR(csp, asmnt)
		self.l1_half_l2 = L1_HALF_L2(csp, asmnt)
		self.alg_ref = {
			"h1":		self.h1,
			"h2":		self.h2,
			"h3":		self.h3,
			"h4":		self.h4,
			"h5":		self.h5,
			"h6":		self.h6,
			"l1_half_l2":	self.l1_half_l2,
			"in_stock": 	self.in_stock,
			"same_th":	self.same_thr,
			"same_r":		self.same_thr,
			"l_dec":		self.l_dec,
			"d_dec":		self.d_dec,
			"len":		self.len
		}

	def var_constraints(self, curvar):
		'''Returns variables that share a constraint with curvar.
		
		Returns a list of constraints that curvar participates in.
		This list is sorted based on the degree that consistency
		algorithms impact varaibles. 
		
		To boost performace, neighbors are cached in self.neighbors.'''
		# c S.F. constraint
		# vc S.F. variable constraints
		if not curvar in self.neighbors:
			o = self.csp.constraint_orders
			self.neighbors[curvar] = [] # order matters
			for c, participants in self.csp.C.items(): 
				if curvar in _vars and not c in self.neighbors[curvar]:
					self.neighbors[curvar].append(c)
			vc = self.neighbors[curvar] 
			self.neighbors[curvar] = sorted(vc, key=lambda c: o[c])
		return self.neighbors[curvar]

	def indirect(self, reduced_vars):
	'''Establishes indirect consistency for reduced_vars.
	
	If the consistency spills over other variables, they are also checked.
	i.e. it establishes consistency for all varaibles recursively.'''
		# psvars S.F. participanting variables
		# rpvars S.F. reduced participanting variables
		impacted = set([])
		i = 0
		while i < len(reduced_vars):
			constraints = self.var_constraints(reduced_vars[i])
			i += 1
			for constraint in constraints:
				psvars = self.csp.C[constraints]
				rpvars = reduced_vars.intersection(psvars)
				res = self.alg_ref[constraint].b_update(rpvars)
				if res[0] == CONTRADICTION:
					return res
				if res[0] == DOMAINS_REDUCED:
					impacted.update(res[1])
					reduced_vars.update(res[1])
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
		
	def direct(self, curvar, value):
		'''Establishes direct consistency for curvar neighbors.
		
		returns a conflict set in case of contradiction or a set of
		variables whose domains have been reduced.
		
		If the domain of a neighbor changes, no further action is taken.
		
		Individual consistency algorithms, detect if there is an oppotunity
		to reduce the domain of their involved variables W.R.T. curvar.
		
		Constraints that have bigger impacts are checked first.'''
		curvar_constraints = self.var_constraints(curvar)
		impacted = set([])
		for c in curvar_constraints:
			res = self.alg_ref[c].establish(curvar, value)
			if res[0] == DOMAINS_REDUCED:	
				impacted.update(res[1])
			elif res[0] == CONTRADICTION:
				return res
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
