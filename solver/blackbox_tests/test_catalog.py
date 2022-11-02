import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from constants import *
from catalog import CATALOG

class test_CATALOG(unittest.TestCase):
    '''Tests the behavior of catalog.'''

    def setUp(self):
        self.__sut = CATALOG()

    def test_correct_values_are_loaded_without_filers(self):
        # arrange
        self.__sut.setup(current+"/real_pieces.csv")
        # act
        T_vals = self.__sut.values("T")
        R_vals = self.__sut.values("R")
        D_vals = self.__sut.values("D")
        l = self.__sut.l()
        # assess
        self.assertEqual(T_vals, {1, 1.5, 2, 2.5, 3, 3.5})
        self.assertEqual(R_vals, {0, 0.5, 1, 1.5, 2, 2.5})
        expected_D_vals = {19, 18, 17.5, 21.5, 21, 20.5, 20, 19.5, 17, 16.5, 16,
            15.5, 15, 14.5, 14, 13.5, 25, 23.5, 18.5, 24}
        self.assertEqual(D_vals, expected_D_vals)
        self.assertEqual(l, 12051)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_CATALOG)
    runner.run(suite)        