import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from sameround import SAMEROUND
from spec import specs
from constants import *

class test_SAMEROUND(unittest.TestCase):
    '''Enfroces same roundness constraint to R variables.

    Partitions:

    a. R1 is not being assigned
    b. At least one of R2, R3, ... to R7 does not contain the value of R1
    c. All variables R2, R3, ... to R7 do contain the value of R1'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SAMEROUND()
    
    def test_contradiction_occurs(self):
        '''R1 = some_value, some_value does not exist in at least one domain.
        
        R1 = 0
        0 does not exist in R2'''
        csp = self.__csp
        csp.update_domain("R1", {0})
        csp.update_domain("R2", {2.5})
        csp.update_domain("R3", {0, 2.5})
        csp.update_domain("R4", {0, 2.5})
        csp.update_domain("R5", {0, 2.5})
        csp.update_domain("R6", {0, 2.5})
        csp.update_domain("R7", {0, 2.5})
        output = self.__sut.establish(csp, "R1", 0)
        self.assertEqual(output[0], CONTRADICTION)
    
    def test_domains_reduce(self):
        '''R1 = some value, some value exists in all domains as well.

        R1 = 2.5
        2.5 exists in all variables'''
        csp = self.__csp
        csp.update_domain("R1", {2.5})
        csp.update_domain("R2", {2.5})
        csp.update_domain("R3", {0, 2.5})
        csp.update_domain("R4", {0, 2.5})
        csp.update_domain("R5", {0, 2.5})
        csp.update_domain("R6", {0, 2.5})
        csp.update_domain("R7", {0, 2.5})
        output = self.__sut.establish(csp, "R1", 2.5)
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"R2", "R3", "R4", "R5", "R6", "R7"})
        D = csp.get_domains()
        for _var in {"R2", "R3", "R4", "R5", "R6", "R7"}:
            self.assertEqual(D[_var], {2.5})

    def test_no_impact(self):
        '''Enforces the case that the algorithm simply does nothing!
        
        The algorithm only checks domains if R1 IS BEING established.
        Otherwise, we are sure that domains are consistent AND further
        reduction is impossible.
        
        The domains remain intact in this case, and they are NOT examined.'''
        csp = self.__csp
        csp.assign("R1", 2.5)
        output = self.__sut.establish(csp, "R2", 2.5)
        self.assertEqual(output, (DOMAINS_INTACT, set([])))

    def test_no_reduction(self):
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