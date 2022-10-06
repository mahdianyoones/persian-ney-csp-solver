import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from hole1 import HOLE1
from spec import specs
from constants import *

class Test_HOLE1(unittest.TestCase):
	'''Tests the behavior of hole1 constraint.'''
			
	def setUp(self):
		self.__csp = CSP()
		self.__sut = HOLE1(specs["C"])

	def __reset_csp(self):
		domain = {"min": 1, "max": 1000}
		for var in {"L1", "L2", "L3"}:
			self.__csp.update_domain(var, domain)	
		self.__csp.unassign_all()		
	
	def test_contradiction_after_propagation(self):
		'''Asserts the occurence of a contradictory case.'''
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
		self.assertEqual(output[1], {"L2", "L3"})

	def test_domains_intact_after_propagation(self):
		'''Asserts that L1, L2, and L3 are examined and remain intact.'''
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
		
	def test_reduction_after_propagation(self):
		'''Asserts a case that domains reduce due to propagation.'''
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
		
	def test_propagate_examines_L1L3(self):
		'''Asserts that only L1 and L3 are examined by propagate.'''
		# arrange
		self.__reset_csp()
		csp = self.__csp
		# act
		output = self.__sut.propagate(csp, {"L2"})
		# assess
		self.assertEqual(output[1], {"L1", "L3"})