import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
grandparent = op.dirname(op.dirname(current))
sp.append(grandparent)

from csp import CSP
from sameround import SAMEROUND
from constants import *

class test_SAMEROUND(unittest.TestCase):
    '''Tests the behavior of sameround constraint.'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SAMEROUND()
    
    def test_establishes_and_reduces(self):
        # arrange
        csp = self.__csp
        domains = {
            "R1": {2.5, 2},
            "R2": {2.5, 5, 4},
            "R3": {0, 2.5},
            "R4": {0, 2.5},
            "R5": {0, 2.5},
            "R6": {0, 2.5},
            "R7": {0, 2.5}
        }
        for var, vals in domains.items():
            csp.update_domain(var, vals)
        # act
        output = self.__sut.establish(csp, "R2", 2.5)
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"R1", "R3", "R4", "R5", "R6", "R7"})
        self.assertEqual(output[2], {"R1", "R3", "R4", "R5", "R6", "R7"})
        D = csp.get_domains()
        self.assertEqual(D["R2"], {2.5, 5, 4})
        for var in {"R1", "R3", "R4", "R5", "R6", "R7"}:
            self.assertEqual(D[var], {2.5})

    def test_contradiction_occurs(self):
        # arrange
        csp = self.__csp
        domains = {
            "R1": {0},
            "R2": {2.5},
            "R3": {0, 2.5},
            "R4": {0, 2.5},
            "R5": {0, 2.5},
            "R6": {0, 2.5},
            "R7": {0, 2.5}
        }
        for var, vals in domains.items():
            csp.update_domain(var, vals)
        # act
        output = self.__sut.establish(csp, "R1", 0)
        # assess
        self.assertEqual(output[0], CONTRADICTION)
    
    def test_establishes_once_only(self):
        '''Enforces the case that the algorithm simply does nothing!
        
        The algorithm only checks domains if THE FIRST R variable is being
        established. Otherwise, we are sure that domains are consistent AND further
        reduction is impossible.
        
        The domains remain intact in this case, and they are NOT examined.'''
        csp = self.__csp
        csp.assign("R1", 2.5)
        output = self.__sut.establish(csp, "R2", 2.5)
        self.assertEqual(output, (DOMAINS_INTACT, set([])))

    def test_all_contain_the_same_value(self):
        '''Enforces a case that domains are checked but no value is removed.
        
        i.e. the domains happend to be just consistent.
        
        The domains remain intact in this case, but they are all examined.'''
        csp = self.__csp
        csp.update_domain("R1", {2.5})
        csp.update_domain("R2", {2.5})
        csp.update_domain("R3", {2.5})
        csp.update_domain("R4", {2.5})
        csp.update_domain("R5", {2.5})
        csp.update_domain("R6", {2.5})
        csp.update_domain("R7", {2.5})
        output = self.__sut.establish(csp, "R1", 2.5)
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertEqual(output[1], {"R2", "R3", "R4", "R5", "R6", "R7"})

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    loader = unittest.defaultTestLoader 
    suite = loader.loadTestsFromTestCase(test_SAMEROUND)
    runner.run(suite)        