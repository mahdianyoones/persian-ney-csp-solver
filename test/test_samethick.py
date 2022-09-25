import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from samethick import SAMETHICK
from spec import specs
from constants import *

class test_SAMETHICK(unittest.TestCase):
    '''Enfroces same thickness constraint to T variables.

    T1 is always assigned first and the rest of variables must'''

    def setUp(self):
        self.__csp = CSP()
        self.__sut = SAMETHICK()
    
    def test_contradiction_occurs(self):
        '''T1 = some_value, some_value does not exist in at least one domain.
        
        T1 = 0
        0 does not exist in T2'''
        csp = self.__csp
        csp.update_domain("T2", {2.5})
        csp.update_domain("T3", {0, 2.5})
        csp.update_domain("T4", {0, 2.5})
        csp.update_domain("T5", {0, 2.5})
        csp.update_domain("T6", {0, 2.5})
        csp.update_domain("T7", {0, 2.5})
        output = self.__sut.establish(csp, "T1", 0)
        self.assertEqual(output[0], CONTRADICTION)
    
    def test_domains_reduce(self):
        '''T1 = some value, some value exists in all domains as well.

        T1 = 2.5
        2.5 exists in all variables'''
        csp = self.__csp
        csp.update_domain("T2", {2.5})
        csp.update_domain("T3", {0, 2.5})
        csp.update_domain("T4", {0, 2.5})
        csp.update_domain("T5", {0, 2.5})
        csp.update_domain("T6", {0, 2.5})
        csp.update_domain("T7", {0, 2.5})
        output = self.__sut.establish(csp, "T1", 2.5)
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"T2", "T3", "T4", "T5", "T6", "T7"})
        D = csp.get_domains()
        for _var in {"T2", "T3", "T4", "T5", "T6", "T7"}:
            self.assertEqual(D[_var], {2.5})

    def test_no_impact(self):
        '''Enforces the case that the algorithm simply does nothing!
        
        The algorithm only checks domains if R1 IS BEING established.
        Otherwise, we are sure that domains are consistent AND further
        reduction is impossible.
        
        The domains remain intact in this case, and they are NOT examined.'''
        csp = self.__csp
        csp.assign("T1", 2.5)
        output = self.__sut.establish(csp, "T2", 2.5)
        self.assertEqual(output, (DOMAINS_INTACT, set([])))

    def test_no_reduction(self):
        '''Enforces a case that domains are checked but no value is removed.
        
        i.e. the domains happend to be just consistent.
        
        The domains remain intact in this case, but they are all examined.'''
        csp = self.__csp
        csp.update_domain("T2", {2.5})
        csp.update_domain("T3", {2.5})
        csp.update_domain("T4", {2.5})
        csp.update_domain("T5", {2.5})
        csp.update_domain("T6", {2.5})
        csp.update_domain("T7", {2.5})
        output = self.__sut.establish(csp, "T1", 2.5)
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertEqual(output[1], {"T2", "T3", "T4", "T5", "T6", "T7"})