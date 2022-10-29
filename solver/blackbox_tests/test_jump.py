import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from jump import JUMP
from spec import specs
from constants import *

class test_JUMP(unittest.TestCase):
    '''Test the behavior of jump.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = JUMP(self.__csp.get_variables())

    def test_accumulates(self):
        # arrange
        csp = self.__csp
        for v in ["D3", "D4", "D2", "D1", "L1", "L2"]:
            csp.assign(v, 2) # arbitrary value
        # act
        self.__sut.accumulate(csp, "L2", {"D2", "D4"})
        confvars = self.__sut.get_confset("L2")
        # assess
        self.assertEqual(confvars, ["D4", "D2"])

    def test_absorbs(self):
        # arrange
        csp = self.__csp
        for v in ["D3", "D4", "D2", "D1", "L1", "L2"]:
            csp.assign(v, 2) # arbitrary value
        self.__sut.accumulate(csp, "D2", {"D4"})
        # act
        self.__sut.absorb(csp, "D2", {"D3"})
        confvars = self.__sut.get_confset("D2")
        # assess
        self.assertEqual(confvars, ["D3", "D4"])

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_JUMP)
    runner.run(suite)