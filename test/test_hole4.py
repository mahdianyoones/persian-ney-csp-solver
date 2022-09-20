import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from hole4 import HOLE4
from spec import specs
from constants import *

class Test_HOLE4(unittest.TestCase):
	'''The goal is to enforce the following constraint relation:

		L1 + L2 + L3 + L4 + S < h4
        
		Each test case represents an equivalence partition.

        S = 30
        h4 = 393

        L1 + L2 + L3 + L4 + 30 < 393

        L1 < 393 - 30 - L2 - L3 - L4
        
        => L1 < 363 - L2 - L3 - L4
	'''
			
	def setUp(self):
		self.__csp = CSP()
		self.__sut = HOLE4(specs["C"])

	def __reset_csp(self):
		domain = {"min": 1, "max": 1000}
		for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
			self.__csp.update_domain(var, domain)	
		self.__csp.unassign_all()		
	
	def test_L1_consistent(self):
		'''Asserts L1 is examined and is consistnet.
		
		Pre-conditions:
		
		min_L1 < h4 - S - A_L2 - A_L4 - L3_curvar

        192 < 393 - 30 - 24 - 24 - 122
        192 < 193
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 192, "max": 192})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		self.assertEqual(output[0], DOMAINS_INTACT)
		self.assertEqual(output[1], {"L1"})
	
	def test_L1_reduces(self):
		'''Asserts that L1 is reduced.
		
		Pre-conditions:
		
		min_L1 < h4 - S - A_L2 - A_L4 - L3_curvar

        192 < 393 - 30 - 24 - 24 - 122
        192 < 193

		max_L1 >= h4 - S - A_L2 - A_L4 - L3_curvar

        193 >= 393 - 40 - 24 - 24 - 122
        193 >= 193

		Lower bound is consistnet.
		Upper bound can be made consistnet.
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 192, "max": 193})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		expected = (DOMAINS_REDUCED, {"L1"}, {"L1"})
		self.assertEqual(output, expected)
		L1 = self.__csp.get_domain("L1")
		self.assertEqual(L1, {"min": 192, "max": 192})

	def test_L1_contradiction(self):
		'''Asserts that L1 cannot be reduced, hence contradiction occurs.
		
		Pre-conditions:
		
		min_L1 >= h4 - S - A_L2 - A_L4 - L3_curvar

        193 >= 393 - 30 - 24 - 24 - 122
        193 >= 193
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 193, "max": 193})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		self.assertEqual(output[1], {"L1"})

	def test_L1L2L3L4_consistent(self):
		'''Asserts that L1, L2, L3, and L4 are consistnet.
		
		Pre-conditions:
		
        L1_max < h4 - L2_min - L3_min - L4_min - S
        L2_max < h4 - L1_min - L3_min - L4_min - S
        L3_max < h4 - L1_min - L2_min - L4_min - S
        L4_max < h4 - L1_min - L2_min - L3_min - S

        192 < 393 - 30 - 24 - 24 - 122

		192 < 193
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 192, "max": 192})
		csp.update_domain("L2", {"min": 24, "max": 24})
		csp.update_domain("L3", {"min": 122, "max": 122})
		csp.update_domain("L4", {"min": 24, "max": 24})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2", "L3"})
		# assess
		expected = (DOMAINS_INTACT, {"L1", "L2", "L3", "L4"})
		self.assertEqual(output, expected)
		
	def test_L1L2L3L4_reduce(self):
		'''Asserts that L1, L2, L3, and L4 get reduced when inconsistent.
		
		Pre-conditions:
		
        L1_max >= h4 - L2_min - L3_min - L4_min - S
        L2_max >= h4 - L1_min - L3_min - L4_min - S
        L3_max >= h4 - L1_min - L2_min - L4_min - S
        L4_max >= h4 - L1_min - L2_min - L3_min - S

        L1_min < h4 - L2_min - L3_min - L4_min - S
        L2_min < h4 - L1_min - L3_min - L4_min - S
        L3_min < h4 - L1_min - L2_min - L4_min - S
        L4_min < h4 - L1_min - L2_min - L3_min - S
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 192, "max": 193})
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
		self.assertEqual(L1, {"min": 192, "max": 192})
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
	
	def test_establish_examines_L3(self):
		'''Asserts that only L3 is examined by establish.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 1)
		csp.assign("L4", 1)
		# act
		output = self.__sut.establish(csp, "L1", 1)
		# assess
		self.assertEqual(output[1], {"L3"})
	
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
		
	def test_propagate_examines_L2(self):
		'''Asserts that only L2 is examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L1", 1)		
		csp.assign("L4", 1)		
		# act
		output = self.__sut.propagate(csp, {"L3"})
		# assess
		self.assertEqual(output[1], {"L2"})
		
	def test_propagate_examines_L3(self):
		'''Asserts that only L3 is examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 1)
		csp.assign("L4", 1)
		# act
		output = self.__sut.propagate(csp, {"L1"})
		# assess
		self.assertEqual(output[1], {"L3"})
		
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
		
	def test_propagate_examines_L2L3(self):
		'''Asserts that only L2 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L4", 1)
		# act
		output = self.__sut.propagate(csp, {"L1"})
		# assess
		self.assertEqual(output[1], {"L2", "L3"})
		
	def test_propagate_examines_L1L2(self):
		'''Asserts that only L1 and L2 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L4", 1)
		# act
		output = self.__sut.propagate(csp, {"L3"})
		# assess
		self.assertEqual(output[1], {"L1", "L2"})

	def test_propagate_examines_L1L2L3(self):
		'''Asserts that only L1, L2 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		# act
		output = self.__sut.propagate(csp, {"L4"})
		# assess
		self.assertEqual(output[1], {"L1", "L2", "L3"})