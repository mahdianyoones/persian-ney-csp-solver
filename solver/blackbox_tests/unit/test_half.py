import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from half import HALF
from spec import specs
from constants import *

class test_HALF(unittest.TestCase):
    '''The goal is to test the behavior of half constraint.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = HALF()

    def test_reduction_after_propagation(self):
        '''Asserts that reduction occurs in propagate entry.'''
        # arrange
        csp = self.__csp
        csp.update_domain("L1", {"min": 30, "max": 36})
        csp.update_domain("L2", {"min": 59, "max": 70})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L1", "L2"})
        self.assertEqual(out[2], {"L1", "L2"})
        D = csp.get_domains()
        self.assertEqual(D["L1"], {"min": 30, "max": 35})
        self.assertEqual(D["L2"], {"min": 60, "max": 70})

    def test_reduction_after_propagation_2(self):
        '''Asserts another case that reduction occurs in propagate entry.'''
        # arrange
        csp = self.__csp
        csp.update_domain("L1", {"min": 19, "max": 30})
        csp.update_domain("L2", {"min": 40, "max": 61})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L1", "L2"})
        self.assertEqual(out[2], {"L1", "L2"})
        D = csp.get_domains()
        self.assertEqual(D["L1"], {"min": 20, "max": 30})
        self.assertEqual(D["L2"], {"min": 40, "max": 60})

    def test_domains_intact_after_propagation(self):
        '''Asserts a case that reduction does not occurs in propagate.'''
        # arrange
        csp = self.__csp
        csp.update_domain("L1", {"min": 20, "max": 30})
        csp.update_domain("L2", {"min": 40, "max": 60})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], DOMAINS_INTACT)
        self.assertEqual(out[1], {"L1", "L2"})

    def test_reduction_after_assignment(self):
        '''Asserts the case that assignment to L1 causes update for L2.'''
        # arrange
        csp = self.__csp
        csp.update_domain("L2", {"min": 59, "max": 61})
        # act
        csp.assign("L1", 30)
        out = self.__sut.establish(csp, "L1", 30)
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L2"})
        self.assertEqual(out[2], {"L2"})
        D = csp.get_domains()
        self.assertEqual(D["L2"], {"min": 60, "max": 60})

    def test_domains_intact_after_assignment(self):
        '''Asserts the case that assignment to L1 causes not update for L2.
        
        i.e. L2 is already consistent (has one value which happens to
        be consistent.'''
        # arrange
        csp = self.__csp
        csp.update_domain("L2", {"min": 60, "max": 60})
        # act
        csp.assign("L1", 30)
        out = self.__sut.establish(csp, "L1", 30)
        # assess
        self.assertEqual(out[0], DOMAINS_INTACT)
        self.assertEqual(out[1], {"L2"})

    def test_contradiction_after_propagation(self):
        '''Asserts that contradiction occurs after propagation.'''
        # arrange
        csp = self.__csp
        csp.update_domain("L1", {"min": 20, "max": 20})
        csp.update_domain("L2", {"min": 41, "max": 70})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L1", "L2"})
        self.assertEqual(out[2], set([]))

    def test_contradiction_after_propagation_2(self):
        '''Asserts another case that contradiction occurs in propagate.'''
        # arrange
        csp = self.__csp
        csp.update_domain("L1", {"min": 40, "max": 70})
        csp.update_domain("L2", {"min": 22, "max": 22})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L1", "L2"})
        self.assertEqual(out[2], set([]))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_HALF)
    runner.run(suite)