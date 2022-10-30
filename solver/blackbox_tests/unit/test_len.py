import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from len import LEN
from spec import specs
from constants import *
import copy

class test_LEN(unittest.TestCase):
    '''Test the behavior of len consistency.'''
    
    def setUp(self):
        self.__csp = CSP()
        len = 524
        self.__sut = LEN(len)
    
    def __set_domains(self):
        domain = {"min": 1, "max": 1000}
        for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            self.__csp.update_domain(var, domain)

    def test_contradiction_after_propagate(self):
        '''Asserts a contradiction case.

        in which sum of the lower bounds are greater than len.'''
        # arrange
        self.__set_domains()
        csp = self.__csp
        csp.update_domain("L1", {"min": 100, "max": 476})
        csp.update_domain("L2", {"min": 100, "max": 86})
        csp.update_domain("L3", {"min": 100, "max": 86})
        csp.update_domain("L4", {"min": 100, "max": 86})
        csp.update_domain("L5", {"min": 100, "max": 86})
        csp.update_domain("L6", {"min": 12, "max": 86})
        csp.update_domain("L7", {"min": 13, "max": 86})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"L1", "L2", "L3", "L4", "L5", "L6", "L7"})
        self.assertEqual(output[2], set([]))

    def test_contradiction_after_propagate_2(self):
        '''Asserts another contradiction case.

        in which sum of the upper bounds are smaller than len.'''
        # arrange
        self.__set_domains()
        csp = self.__csp
        csp.update_domain("L1", {"min": 1, "max": 100})
        csp.update_domain("L2", {"min": 1, "max": 100})
        csp.update_domain("L3", {"min": 1, "max": 100})
        csp.update_domain("L4", {"min": 1, "max": 100})
        csp.update_domain("L5", {"min": 1, "max": 100})
        csp.update_domain("L6", {"min": 1, "max": 12})
        csp.update_domain("L7", {"min": 1, "max": 11})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"L1", "L2", "L3", "L4", "L5", "L6", "L7"})
        self.assertEqual(output[2], set([]))

    def test_contradiction_after_establish(self):
        '''Assers a contradictory case.'''
        # arrange
        self.__set_domains()
        csp = self.__csp
        csp.assign("L1", 100)
        csp.assign("L2", 100)
        csp.assign("L3", 100)
        csp.assign("L4", 100)
        csp.assign("L5", 100)
        csp.assign("L6", 20)
        csp.update_domain("L7", {"min": 5, "max": 100})
        # act
        output = self.__sut.establish(csp, "L6", 9)
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"L7"})
        self.assertEqual(output[2], {"L1","L2","L3","L4","L5","L6"})

    def test_contradiction_after_establish_2(self):
        '''Assers a contradictory case.'''
        # arrange
        self.__set_domains()
        csp = self.__csp
        csp.assign("L1", 100)
        csp.assign("L2", 100)
        csp.assign("L3", 100)
        csp.assign("L4", 100)
        csp.assign("L5", 100)
        csp.assign("L6", 20)
        csp.update_domain("L7", {"min": 1, "max": 3})
        # act
        output = self.__sut.establish(csp, "L6", 9)
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"L7"})
        self.assertEqual(output[2], {"L1","L2","L3","L4","L5","L6"})

    def test_domains_reduce_establish(self):
        '''Asserts the domain occurs.'''
        # arrange
        self.__set_domains()
        csp = self.__csp
        csp.assign("L7", 100)
        csp.assign("L2", 100)
        csp.assign("L3", 100)
        csp.assign("L4", 100)
        csp.assign("L5", 100)
        csp.assign("L6", 20)
        csp.update_domain("L1", {"min": 3, "max": 5})
        # act
        output = self.__sut.establish(csp, "L6", 9)
        # assess
        self.assertEqual(output[0], DOMAIN_REDUCED)
        self.assertEqual(output[1], {"L1"})
        self.assertEqual(output[2], {"L1"})
        L1 = csp.get_domain("L1")
        self.assertEqual(L1, {"min": 4, "max": 4})

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_LEN)
    runner.run(suite)