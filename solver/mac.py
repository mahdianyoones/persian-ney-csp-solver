from hole1 import HOLE1
from hole3 import HOLE3
from hole6 import HOLE6
from len import LEN
from lendec import LENDEC
from lendec_lower import LENDEC_LOWER
from diamdec import DIAMDEC
from samethick import SAMETHICK
from sameround import SAMEROUND
from half import HALF
from stock import STOCK
from constants import *

class MAC():
	'''Implements MAC through special consistency algorithms.'''

	def __init__(self, csp, catalog, spec):
		self.__csp = csp
		self.__X2C = {}
		self.__constraints_order = {}
		self.__init_c_order(csp)
		self.__init_X2C(csp)
		stock_ref = STOCK(catalog)
		self.__refs = {
			"hole1":		HOLE1(spec["h1"], spec["hmarg"]),
			"hole3":		HOLE3(spec["h3"], spec["hmarg"]),
			"hole6":		HOLE6(spec["h6"], spec["hmarg"]),
			"half":			HALF(),
			"stock1": 		stock_ref,
			"stock2": 		stock_ref,
			"stock3": 		stock_ref,
			"stock4": 		stock_ref,
			"stock5": 		stock_ref,
			"stock6": 		stock_ref,
			"stock7": 		stock_ref,
			"samethick":	SAMETHICK(),
			"sameround":	SAMEROUND(),
			"lendec":		LENDEC(),
			"lendec_lower":	LENDEC_LOWER(),
			"diamdec":		DIAMDEC(spec["ddiff"]),
			"len":			LEN(spec["len"])
		}

	def establish(self, curvar, value):
		'''Establishes consistency after var: value assignment.
		
		Calls all the consistency algorithms of the constraints on curvar, and
		returns a conflict set in case of contradiction or reduced_vars, which
		is a set of variables whose domains have been reduced.

		The effect of domain reductions is then kept in check by the
		upper subroutine calling the propagate method.
		
		Constraints that may have bigger impacts are called first.'''
		csp = self.__csp
		constraints = self.__X2C[curvar]
		reduced_vars = set([])
		examined = set([])
		evaled_consts = set([])
		for constraint in constraints:
			evaled_consts.add(constraint)
			ref = self.__refs[constraint]
			res = ref.establish(csp, curvar, value)
			examined.update(res[1])
			if res[0] == DOMAINS_REDUCED: 	
				reduced_vars.update(res[2])
			elif res[0] == CONTRADICTION:
				return (CONTRADICTION, examined, res[2], evaled_consts)
		if len(reduced_vars) > 0:
			return (DOMAINS_REDUCED, examined, reduced_vars, evaled_consts)
		return (DOMAINS_INTACT, set([]), evaled_consts)

	def propagate(self, reduced_vars):
		'''Recursively propagates domain reductions.'''
		csp = self.__csp
		evaled_consts = set([])
		new_reduced_vars = set([])
		examined = set([])
		while len(reduced_vars) > 0:
			_var = reduced_vars.pop()
			constraints = self.__X2C[_var]
			for constraint in constraints:
				evaled_consts.add(constraint)
				participants = csp.get_neighbors(constraint)
				reduced_prtcns = reduced_vars.intersection(participants)
				reduced_prtcns.add(_var)
				res = self.__refs[constraint].propagate(csp, reduced_prtcns)
				examined.update(res[1])
				if res[0] == CONTRADICTION:
					return (CONTRADICTION, examined, res[2], evaled_consts)
				if res[0] == DOMAINS_REDUCED:
					new_reduced_vars.update(res[2])
					reduced_vars.update(res[2])
		return (PROPAGATION_PROCEEDED, new_reduced_vars, evaled_consts)
	
	def __init_c_order(self, csp):
		'''Determines the order of constraints.
		
		A constraint order denotes the number of participants it has.'''
		constraints = csp.get_constraints()
		for constraint, participants in constraints.items():
			self.__constraints_order[constraint] = 8 - len(participants)

	def __init_X2C(self, csp):
		'''Buils a map from each variable to the constraints they participate.
		
		Constraints of each variable are sorted based on their order.'''
		C = csp.get_constraints()
		X = csp.get_variables()
		X2C = {}
		corders = self.__constraints_order
		for constraint, _vars in C.items():
			for v in X:
				if not v in X2C:
					X2C[v] = set([])
				if v in _vars:
					X2C[v].add(constraint)
		for v, constraints in X2C.items():
			self.__X2C[v] = sorted(constraints, key=lambda c: corders[c])