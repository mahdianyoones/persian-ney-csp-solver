import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from catalog import CATALOG
from spec import specs
from csp import CSP
from unary import UNARY

class Test_INIT_DOMAIN(unittest.TestCase):
	
	def setUp(self):
		self.__sut = CSP()
		catalog = CATALOG()
		catalog.setup("measures_of_drained_pieces.csv")
		unary = UNARY()
		unary.unarify(self.__sut, catalog, specs["C"])
	
	def testD1InitialDomain(self):
		expected = { 18.0, 18.5, 19.0, 19.5, 20.0,
		  		   20.5, 21.0, 21.5, 23.5, 24.0}
		self.assertEqual(self.__sut.get_domain("D1"), expected)				
	
	def testDvarsInitialDomain(self):
		expected = { 13.5, 14.0, 14.5, 15.0,
				   15.5, 16.0, 16.5, 17.0, 17.5,
				   18.0, 18.5, 19.0, 19.5, 20.0,
		  		   20.5, 21.0, 21.5, 23.5, 24.0, 
		  		   25.0}
		for var in {"D2", "D3", "D4", "D5", "D6", "D7"}:
			var_domain = self.__sut.get_domain(var)
			self.assertEqual(var_domain, expected)
	
	def testTvarsInitialDomain(self):
		expected = {1.0, 1.5, 2.0, 2.5, 3.0, 3.5}
		for var in {"T1", "T2", "T3", "T4", "T5", "T6", "T7"}:
			var_domain = self.__sut.get_domain(var)
			self.assertEqual(var_domain, expected)
	
	def testRvarsInitialDomain(self):
		expected = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5}
		for var in {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}:
			var_domain = self.__sut.get_domain(var)
			self.assertEqual(var_domain, expected)
	
	def testLvarsInitialDomain(self):
		L1 = self.__sut.get_domain("L1")
		L2 = self.__sut.get_domain("L2")
		L3 = self.__sut.get_domain("L3")
		L4 = self.__sut.get_domain("L4")
		L5 = self.__sut.get_domain("L5")
		L6 = self.__sut.get_domain("L6")
		L7 = self.__sut.get_domain("L7")
		self.assertEqual(L1["min"], 20)		
		self.assertEqual(L2["min"], 20)		
		self.assertEqual(L3["min"], 20)		
		self.assertEqual(L4["min"], 50)		
		self.assertEqual(L5["min"], 70)		
		self.assertEqual(L6["min"], 30)		
		self.assertEqual(L7["min"], 20)
