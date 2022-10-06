from hole1 import HOLE1A
from hole1B import HOLE1B
from hole2 import HOLE2
from hole3 import HOLE3
from hole4 import HOLE4
from hole5 import HOLE5
from hole6 import HOLE6
from len import LEN
from lendec import LENDEC
from diamdec import DIAMDEC
from samethick import SAMETHICK
from sameround import SAMEROUND
from half import HALF
from stock import STOCK
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
	def __init__(self, csp):
		self.__csp = csp
		self.__neighbors = {}
		self._constraints_order = {}
		self.__init_constraints_order(csp)
		self.__alg_refs = {
			"hole1A":		HOLE1A(csp),
			"hole1B":		HOLE1B(csp),
			"h2":		H2(csp),
			"h3":		H3(csp),
			"h4":		H4(csp),
			"h5":		H5(csp),
			"h6":		H6(csp),
			"l1_half_l2":	sL1_HALF_L2(csp),
			"in_stock": 	IN_STOCK(csp),
			"same_th":	self.__same_th,
			"same_r":		self.__same_r,
			"l_dec":		L_DEC(csp),
			"d_dec":		D_DEC(csp),
			"len":		LEN(csp)
		}

	def __init_constraints_order(self, csp):
		'''Determines the order of constraints.
		
		A constraint order denotes the number of participants it has.'''
		constraints = csp.get_constraints()
		for constraint, participants in constraints:
			self.__constraints_order[constraint] = 8 - len(participants)

	def __var_constraints(self, var):
		'''Returns variables that share a constraint with curvar.
		
		Returns a list of constraints that curvar participates in.
		This list is sorted based on the degree that consistency
		algorithms impact varaibles. 
		
		To boost performace, neighbors are cached in self.neighbors.
		This is a mathematical function.'''
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
		impacted = set([])
		i = 0
		while i < len(reduced_vars):
			constraints = self.var_constraints(reduced_vars[i])
			i += 1
			for constraint in constraints:
				participants = self.__csp.get_participants(constraint)
				reduced_vars = reduced_vars.intersection(participants)
				res = self.alg_ref[constraint].b_update(reduced_vars)
				if res[0] == CONTRADICTION:
					return res
				if res[0] == DOMAINS_REDUCED:
					impacted.update(res[1])
					reduced_vars.update(res[1])
		if len(impacted) > 0:
			return (DOMAINS_REDUCED, impacted)
		return (DOMAINS_INTACT, set([]))
		
	def direct(self, var, value):
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
