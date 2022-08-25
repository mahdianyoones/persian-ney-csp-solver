import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from catalog import CATALOG

class TestINIT_THRD(unittest.TestCase):
	
	def setUp(self):
		self.__sut = CATALOG()
		self.__sut.setup("measures_of_drained_pieces.csv")
	
	def testD(self):
		D_values = { 13.5, 14.0, 15.0, 14.5, 
				   15.5, 18.5, 16.5, 17.5, 
		  		   18.0, 19.0, 20.5, 21.0, 
		  		   21.5, 20.0, 19.5, 23.5, 
		  		   25.0, 24.0, 16.0, 17.0, 
		  		   18.5, 18.0, 19.0, 20.5, 
		  		   21.0, 21.5, 20.0, 19.5, 
		  		   23.5, 24.0 }
		returned_values = self.__sut.values("D")
		self.assertEqual(D_values, returned_values)
	
	def testTH(self):
		TH_values = {1.0, 1.5, 2.0, 2.5, 3.0, 3.5}
		returned_values = self.__sut.values("TH")
		self.assertEqual(TH_values, returned_values)
	
	def testR(self):
		R_values = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5}
		returned_values = self.__sut.values("R")
		self.assertEqual(R_values, returned_values)
