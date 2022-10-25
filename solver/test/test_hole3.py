import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from hole3 import HOLE3
from spec import specs
from constants import *
import copy

class Test_HOLE3(unittest.TestCase):
	'''The goal is to enforce the following constraint relation:

		L1 + L2 + L3 + L4 + S < h3
        
		Each test case represents one or more equivalence partition.'''
			
	def setUp(self):
		self.__csp = CSP()
		spec = copy.deepcopy(specs["C"])
		spec["hmarg"] = 10
		self.__sut = HOLE3(spec["h3"], spec["hmarg"])

	def __reset_csp(self):
		domain = {"min": 1, "max": 1000}
		for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
			self.__csp.update_domain(var, domain)	
		self.__csp.unassign_all()		
	
	def test_L1_contradiction(self):
		'''Asserts that L1 cannot be reduced, hence contradiction occurs.
		
		Pre-conditions:
		
		min_L1 >= h3 - S - A_L2 - A_L4 - L3_curvar

        191 >= 371 - 10 - 24 - 24 - 122
        191 >= 191
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L3", 122)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 191, "max": 191})
		# act
		output = self.__sut.establish(csp, "L4", 24)
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		self.assertEqual(output[1], {"L1"})
		self.assertEqual(output[2], {"L2", "L3", "L4"})

	def test_all_consistent(self):
		'''Asserts that L1, L2, L3, and L4 are consistnet.
		
		Pre-conditions:
		
        L1_max < h3 - L2_min - L3_min - L4_min - S
        L2_max < h3 - L1_min - L3_min - L4_min - S
        L3_max < h3 - L1_min - L2_min - L4_min - S
        L4_max < h3 - L1_min - L2_min - L3_min - S

        190 < 371 - 10 - 24 - 24 - 122

		190 < 191
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 190, "max": 190})
		csp.update_domain("L2", {"min": 24, "max": 24})
		csp.update_domain("L3", {"min": 122, "max": 122})
		csp.update_domain("L4", {"min": 24, "max": 24})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2", "L3"})
		# assess
		expected = (DOMAINS_INTACT, {"L1", "L2", "L3", "L4"})
		self.assertEqual(output, expected)
		
	def test_all_reduce(self):
		'''Asserts that L1, L2, L3, and L4 get reduced when inconsistent.
		
		Pre-conditions:
		
        L1_max >= h3 - L2_min - L3_min - L4_min - S
        L2_max >= h3 - L1_min - L3_min - L4_min - S
        L3_max >= h3 - L1_min - L2_min - L4_min - S
        L4_max >= h3 - L1_min - L2_min - L3_min - S

        L1_min < h3 - L2_min - L3_min - L4_min - S
        L2_min < h3 - L1_min - L3_min - L4_min - S
        L3_min < h3 - L1_min - L2_min - L4_min - S
        L4_min < h3 - L1_min - L2_min - L3_min - S
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 190, "max": 191})
		csp.update_domain("L2", {"min": 24, "max": 25})
		csp.update_domain("L3", {"min": 122, "max": 123})
		csp.update_domain("L4", {"min": 24, "max": 25})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2", "L3"})
		# assess
		self.assertEqual(output[0], DOMAINS_REDUCED)
		self.assertEqual(output[1], {"L1", "L2", "L3", "L4"})
		self.assertEqual(output[2], {"L1", "L2", "L3", "L4"})
		L1 = self.__csp.get_domain("L1")
		L2 = self.__csp.get_domain("L2")
		L3 = self.__csp.get_domain("L3")
		L4 = self.__csp.get_domain("L4")
		self.assertEqual(L1, {"min": 190, "max": 190})
		self.assertEqual(L2, {"min": 24, "max": 24})
		self.assertEqual(L3, {"min": 122, "max": 122})
		self.assertEqual(L4, {"min": 24, "max": 24})
		
	def test_establish_examines_L2(self):
		'''Asserts that only L2 is examined by establish.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L1", 1)		
		csp.assign("L4", 1)		
		# act
		output = self.__sut.establish(csp, "L3", 1)
		# assess
		self.assertEqual(output[1], {"L2"})
	
	def test_propagate_examines_L1(self):
		'''Asserts that only L1 is examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 1)	
		csp.assign("L4", 1)	
		# act
		output = self.__sut.propagate(csp, {"L3"})
		# assess
		self.assertEqual(output[1], {"L1"})
			
	def test_propagate_examines_L1L3(self):
		'''Asserts that only L1 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L4", 1)
		# act
		output = self.__sut.propagate(csp, {"L2"})
		# assess
		self.assertEqual(output[1], {"L1", "L3"})
		
	def test_propagate_examines_L1L2L3(self):
		'''Asserts that only L1, L2 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		# act
		output = self.__sut.propagate(csp, {"L4"})
		# assess
		self.assertEqual(output[1], {"L1", "L2", "L3"})
