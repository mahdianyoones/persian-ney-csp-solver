import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from lendec import LENDEC
from spec import specs
from constants import *

class test_LENDEC(unittest.TestCase):
    '''Tests the behavior of len decrement consistency.
    
    The following inequalities are established between variables L2 to L7:
    L2 > L3
    L3 > L4
    L4 > L5
    L5 > L6
    L6 > L7'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = LENDEC()
    
    def __reset_csp(self):
        self.__csp.unassign_all()

    def test_propagate_reduces_bounds(self):
        '''A case that all inconsistency conditions exist and are fixed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L2", {"min": 41, "max": 50})     # to 42, 50
        csp.update_domain("L3", {"min": 41, "max": 50})     # to 41, 49
        csp.update_domain("L4", {"min": 40, "max": 49})     # to 40, 48
        csp.update_domain("L5", {"min": 39, "max": 47})     # examined, intact
        csp.update_domain("L6", {"min": 38, "max": 48})     # to 38, 46
        csp.update_domain("L7", {"min": 37, "max": 45})     # examined, intact
        # act
        out = self.__sut.propagate(csp, {"L2", "L6"})
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L2", "L3", "L4", "L5", "L6", "L7"})
        self.assertEqual(out[2], {"L2", "L3", "L4", "L6"})
        self.assertEqual(D["L2"], {"min": 42, "max": 50})
        self.assertEqual(D["L3"], {"min": 41, "max": 49})
        self.assertEqual(D["L4"], {"min": 40, "max": 48})
        self.assertEqual(D["L6"], {"min": 38, "max": 46})

    def test_establish_reduces_bounds(self):
        '''Another case in which inconsisten values are removed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 50)
        csp.update_domain("L3", {"min": 48, "max": 50})     # to 48, 49
        csp.update_domain("L4", {"min": 47, "max": 49})     # to 47, 48
        csp.assign("L5", 46)
        # act
        out = self.__sut.establish(csp, "L2", 50)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L3", "L4"})
        self.assertEqual(out[2], {"L3", "L4"})
        self.assertEqual(D["L3"], {"min": 48, "max": 49})
        self.assertEqual(D["L4"], {"min": 47, "max": 48})

    def test_contradiction_occurs_after_establish(self):
        '''A case in which contradiction occurs.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L3", {"min": 50, "max": 50}) # min cannot become 49
       # act
        csp.assign("L2", 50)
        out = self.__sut.establish(csp, "L2", 50)
        # assess
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[2], {"L2"})

    def test_contradiction_occurs_after_propagate(self):
        '''A case that all inconsistency conditions exist and are fixed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L2", {"min": 50, "max": 100})     # examined
        csp.update_domain("L3", {"min": 50, "max": 100})     # examined
        csp.update_domain("L4", {"min": 50, "max": 100})     # examined
        csp.update_domain("L5", {"min": 50, "max": 100})     # examined
        csp.update_domain("L6", {"min": 50, "max": 100})     # examined
        csp.update_domain("L7", {"min": 100, "max": 100})     # contradiction
        # act
        out = self.__sut.propagate(csp, {"L2"})
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L2", "L3", "L4", "L5", "L6", "L7"})
        self.assertEqual(out[2], set([]))
