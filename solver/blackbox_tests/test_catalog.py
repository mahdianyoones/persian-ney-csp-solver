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
        self.__sut.setup(current+"/catalog.csv")

    def test_returns_correct_thick_without_filters(self):
        # act
        T_vals = self.__sut.values("T")
        # assess
        self.assertEqual(T_vals, {2, 2.5})

    def test_returns_correct_thick_with_filters(self):
        # act
        T_vals = self.__sut.values("T", {"D": 13, "R": 0})
        # assess
        self.assertEqual(T_vals, {2.0, 2.5})
        # act
        T_vals = self.__sut.values("T", {"D": 13, "R": 1})
        # assess
        self.assertEqual(T_vals, {2})

    def test_returns_correct_round_without_filters(self):
        # act
        R_vals = self.__sut.values("R")
        # assess
        self.assertEqual(R_vals, {0, 1})

    def test_returns_correct_round_with_filters(self):
        # act
        R_vals = self.__sut.values("R", {"D": 12.4})
        # assess
        self.assertEqual(R_vals, {0})

    def test_returns_correct_diamter_without_filters(self):
        # act
        D_vals = self.__sut.values("D")
        # assess
        expected_D_vals = {19, 18, 17, 16, 15, 14, 13, 12.4}
        self.assertEqual(D_vals, expected_D_vals)

    def test_returns_correct_diamter_with_filters(self):
        # act
        D_vals = self.__sut.values("D", {"T": 2, "R": 1})
        # assess
        expected_D_vals = {13}
        self.assertEqual(D_vals, expected_D_vals)

    def test_returns_correct_pieces_without_filters(self):
        # act
        pieces = self.__sut.pieces()
        # assess
        expected_pieces = {
            ("1", 100), 
            ("2", 200), 
            ("3", 80),
            ("4", 70), 
            ("5", 150), 
            ("6", 130), 
            ("7", 60), 
            ("8", 170), 
            ("9", 220), 
            ("10", 300), 
            ("11", 120)
        }
        self.assertEqual(pieces, expected_pieces)

    def test_returns_correct_pieces_with_filters(self):
        # act
        pieces = self.__sut.pieces({"T": 2, "R": 0})
        # assess
        expected_pieces = {
            ("1", 100), 
            ("2", 200), 
            ("3", 80),
            ("4", 70), 
            ("5", 150), 
            ("6", 130), 
            ("7", 60), 
            ("10", 300), 
            ("11", 120)
        }
        self.assertEqual(pieces, expected_pieces)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_CATALOG)
    runner.run(suite)        