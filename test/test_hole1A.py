import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from hole1A import HOLE1A
from spec import specs
from constants import *

class Test_HOLE1A(unittest.TestCase):
	'''The goal is to enforce the following constraint relation:

		L1 + L2 + L3 + S < h1
        
		Each test case represents an equivalence partition.		
	'''
			
	def setUp(self):
		self.__csp = CSP()
		self.__sut = HOLE1A(specs["C"])

	def __reset_csp(self):
		domain = {"min": 1, "max": 1000}
		for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
			self.__csp.update_domain(var, domain)	
		self.__csp.unassign_all()		
	
	def test_L1_consistent(self):
		'''Asserts L1 is examined and is consistnet.

		Pre-conditions:

		min_L1 < h1 - S - A_L2 - L3_curvar
 		max_L1 < h1 - s - A_L2 - L3_curvar
		min_L1 <= max_L1		
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 48)
		csp.update_domain("L1", {"min": 131, "max": 131})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		self.assertEqual(output[0], DOMAINS_INTACT)
		self.assertEqual(output[1], {"L1"})
	
	def test_L1_reduces(self):
		'''Asserts that L1 is reduced.
		
		Pre-conditions:
		
		min_L1 < h1 - S - (A_L2 + L3_curvar)

		max_L1 => h1 - s - (A_L2 + L3_curvar)
		
		Lower bound is consistnet.
		Upper bound can be made consistnet.
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 48)
		csp.update_domain("L1", {"min": 131, "max": 132})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		expected = (DOMAINS_REDUCED, {"L1"}, {"L1"})
		self.assertEqual(output, expected)
		L1 = self.__csp.get_domain("L1")
		self.assertEqual(L1, {"min": 131, "max": 131})

	def test_L1_contradiction(self):
		'''Asserts that L1 cannot be reduced, hence contradiction occurs.
		
		Pre-conditions:
		
		Min_L1 >= h1 - S - (A_L2 + L3_curvar)

		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 48)
		csp.update_domain("L1", {"min": 132, "max": 132})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		self.assertEqual(output[1], {"L1"})

	def test_L1L2L3_consistent(self):
		'''Asserts that L1, L2, and L3 are consistnet.
		
		Pre-conditions:
		
		min_L1 < h1 - S - (min_L2 + min_L3)
		min_L2 < h1 - S - (min_L1 + min_L3)
		min_L3 < h1 - S - (min_L1 + min_L2)
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 131, "max": 131})
		csp.update_domain("L2", {"min": 48, "max": 48})
		csp.update_domain("L3", {"min": 122, "max": 122})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2"})
		# assess
		expected = (DOMAINS_INTACT, {"L1", "L2", "L3"})
		self.assertEqual(output, expected)
		
	def test_L1L2L3_reduce(self):
		'''Asserts that L1, L2, and L3 get reduced when inconsistent.
		
		Pre-conditions:
		
		max_L1 => h1 - S - (min_L2 + min_L3)
		max_L2 => h1 - S - (min_L1 + min_L3)
		max_L3 => h1 - S - (min_L1 + min_L2)

		min_L1 < h1 - S - (min_L2 + min_L3)
		min_L2 < h1 - S - (min_L1 + min_L3)
		min_L3 < h1 - S - (min_L1 + min_L2)
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 131, "max": 132})
		csp.update_domain("L2", {"min": 48, "max": 49})
		csp.update_domain("L3", {"min": 122, "max": 123})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2"})
		# assess
		expected = (DOMAINS_REDUCED, {"L1", "L2", "L3"}, {"L1", "L2", "L3"})
		self.assertEqual(output, expected)
		L1 = self.__csp.get_domain("L1")
		L2 = self.__csp.get_domain("L2")
		L3 = self.__csp.get_domain("L3")
		self.assertEqual(L1, {"min": 131, "max": 131})
		self.assertEqual(L2, {"min": 48, "max": 48})
		self.assertEqual(L3, {"min": 122, "max": 122})
		
	def test_L1L2L3_contradiction(self):
		'''Asserts that L1, L2, and L3 cannot be reduced; contradiction.
		
		min_L1 >= h1 - S - (min_L2 + min_L3)
		min_L2 >= h1 - S - (min_L1 + min_L3)
		min_L3 >= h1 - S - (min_L1 + min_L2)
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 132, "max": 132})
		csp.update_domain("L2", {"min": 48, "max": 48})
		csp.update_domain("L3", {"min": 122, "max": 122})
		# act
		output = self.__sut.propagate(csp, {"L1"})
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		# act
		output = self.__sut.propagate(csp, {"L2"})
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		# act
		output = self.__sut.propagate(csp, {"L3"})
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		
	def test_establish_examines_L2(self):
		'''Asserts that only L2 is examined by establish.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L1", 1)		
		# act
		output = self.__sut.establish(csp, "L3", 1)
		# assess
		self.assertEqual(output[1], {"L2"})
		
	def test_establish_examines_L2(self):
		'''Asserts that only L2 is examined by establish.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L1", 1)		
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
		# act
		output = self.__sut.propagate(csp, {"L1"})
		# assess
		self.assertEqual(output[1], {"L3"})
		
	def test_propagate_examines_L1L3(self):
		'''Asserts that only L1 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		# act
		output = self.__sut.propagate(csp, {"L2"})
		# assess
		self.assertEqual(output[1], {"L1", "L3"})
		
	def test_propagate_examines_L2L3(self):
		'''Asserts that only L2 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		# act
		output = self.__sut.propagate(csp, {"L1"})
		# assess
		self.assertEqual(output[1], {"L2", "L3"})
		
	def test_propagate_examines_L1L2(self):
		'''Asserts that only L1 and L2 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		# act
		output = self.__sut.propagate(csp, {"L3"})
		# assess
		self.assertEqual(output[1], {"L1", "L2"})