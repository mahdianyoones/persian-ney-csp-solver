import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from hole1B import HOLE1B
from spec import specs
from constants import *

class Test_HOLE1B(unittest.TestCase):
	'''The goal is to enforce the following constraint relation:

		L1 + L2 + L3 + L4 - 10 > h1
		
		122 + 24 + 131 + 24 - 10 > 312
	'''
			
	def setUp(self):
		self.__csp = CSP()
		self.__sut = HOLE1B(specs["C"])

	def __reset_csp(self):
		domain = {"min": 1, "max": 1000}
		for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
			self.__csp.update_domain(var, domain)	
		self.__csp.unassign_all()		
	
	def test_L1_consistent(self):
		'''Asserts L1 is examined and remains intact.
		
		Pre-conditions:
		
		L1 < h1 - S - L2 - L3 - L4		
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 1, "max": 131})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		expected = (DOMAINS_INTACT, {"L1"}, set([]))
		self.assertEqual(output, expected)
	
	def test_L1_reduces(self):
		'''Asserts that only L1 is reduced.
		
		Pre-conditions:
		
		L1 = h1 - S - L2 - L3 - L4
		L1_min < L1_max
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 131, "max": 132})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		expected = (DOMAINS_REDUCED, {"L1"}, {"L1"})
		self.assertEqual(output, expected)
		L1 = self.__csp.get_domains("L1")
		self.assertEqual(L1, {"min": 131, "max": 131})
	
	def test_L1_reduces_2(self):
		'''Asserts that only L1 is reduced.
		
		Pre-conditions:
		
		L1 > h1 - S - L2 - L3 - L4
		L1_min + 1 < L1_max
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 130, "max": 132})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		expected = (DOMAINS_REDUCED, {"L1"}, {"L1"})
		self.assertEqual(output, expected)
		L1 = self.__csp.get_domains("L1")
		self.assertEqual(L1, {"min": 130, "max": 131})

	def test_L1_contradiction(self):
		'''Asserts that L1 cannot be reduced, hence contradiction occurs.
		
		Pre-conditions:
		
		L1 = h1 - S - L2 - L3 - L4
		L1_max = L1_min
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 132, "max": 132})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		self.assertEqual(output[1], {"L1"})
	
	def test_L1_contradiction_2(self):
		'''Asserts that L1 cannot be reduced, hence contradiction occurs.
		
		Pre-conditions:
		
		L1 > h1 - S - L2 - L3 - L4
		L1_min + 1 = L1_max
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.assign("L2", 24)
		csp.assign("L4", 24)
		csp.update_domain("L1", {"min": 132, "max": 133})
		# act
		output = self.__sut.establish(csp, "L3", 122)
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		self.assertEqual(output[1], {"L1"})

	def test_L1L2L3L4_consistent(self):
		'''Asserts that L1, L2, L3, and L4 are consistnet.
		
		Pre-conditions:
		
		L1 < 312 – (L2 + L3 + L4)
		L2 < 312 – (L1 + L3 + L4)
		L3 < 312 – (L1 + L2 + L4)		
		L4 < 312 – (L1 + L2 + L3)		
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 1, "max": 131})
		csp.update_domain("L2", {"min": 1, "max": 24})
		csp.update_domain("L3", {"min": 1, "max": 122})
		csp.update_domain("L4", {"min": 1, "max": 24})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2", "L3"})
		# assess
		expected = (DOMAINS_INTACT, {"L1", "L2", "L3", "L4"}, set([]))
		self.assertEqual(output, expected)
		
	def test_L1L2L3_reduce(self):
		'''Asserts that L1, L2, L3, and L4 get reduced when inconsistent.
		
		Pre-conditions:
		
		L1 = 312 – (L2 + L3 + L4)
		L2 = 312 – (L1 + L3 + L4)
		L3 = 312 – (L1 + L2 + L4)
		L4 = 312 - (L1 + L2 + L3)
		min < max (for all)		
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 131, "max": 132})
		csp.update_domain("L2", {"min": 47, "max": 48})
		csp.update_domain("L3", {"min": 121, "max": 122})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2"})
		# assess
		expected = (DOMAINS_REDUCED, {"L1", "L2", "L3"}, {"L1", "L2", "L3"})
		self.assertEqual(output, expected)
		L1 = self.__csp.get_domains("L1")
		L2 = self.__csp.get_domains("L2")
		L3 = self.__csp.get_domains("L3")
		self.assertEqual(L1, {"min": 131, "max": 131})
		
	def test_L1L2L3_reduce_2(self):
		'''Asserts that L1, L2, and L3 get reduced when inconsistent.
		
		Pre-conditions:
		
		L1 > 312 – (L2 + L3)
		L2 > 312 – (L1 + L3)
		L3 > 312 – (L1 + L2)
		min + 1 < max
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 131, "max": 133})
		csp.update_domain("L2", {"min": 46, "max": 48})
		csp.update_domain("L3", {"min": 120, "max": 122})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2"})
		# assess
		expected = (DOMAINS_REDUCED, {"L1", "L2", "L3"}, {"L1", "L2", "L3"})
		self.assertEqual(output, expected)
	
	def test_L1L2L3_contradiction(self):
		'''Asserts that L1, L2, and L3 cannot be reduced; contradiction.
		
		L1 = 312 – (L2 + L3)
		L2 = 312 – (L1 + L3)
		L3 = 312 – (L1 + L2)
		min = max
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 132, "max": 132})
		csp.update_domain("L2", {"min": 48, "max": 48})
		csp.update_domain("L3", {"min": 122, "max": 122})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2"})
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		self.assertEqual(output[], {"L1", "L2", "L3"})

	def test_L1L2L3_contradiction_2(self):
		'''Asserts that L1, L2, and L3 cannot be reduced; contradiction.
		
		L1 > 312 – (L2 + L3)
		L2 > 312 – (L1 + L3)
		L3 > 312 – (L1 + L2)
		min + 1 = max
		'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		csp.update_domain("L1", {"min": 130, "max": 131})
		csp.update_domain("L2", {"min": 47, "max": 48})
		csp.update_domain("L3", {"min": 121, "max": 122})
		# act
		output = self.__sut.propagate(csp, {"L1", "L2"})
		# assess
		self.assertEqual(output[0], CONTRADICTION)
		self.assertEqual(output[1], {"L1", "L2", "L3"})

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
		
	def test_propagate_examines_L1L2L3(self):
		'''Asserts that only L1, L2 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		# act
		output = self.__sut.propagate(csp, {"L1", "L2"})
		# assess
		self.assertEqual(output[1], {"L1", "L2", "L3"})
		
