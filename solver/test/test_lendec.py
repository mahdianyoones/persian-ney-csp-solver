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
        '''A case in which propagate detects and removes inconsistent values.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L2", {"min": 50, "max": 100})    # to 49, 99
        csp.update_domain("L3", {"min": 49, "max": 99})     # to 48, 98
        csp.update_domain("L4", {"min": 48, "max": 98})     # to 47, 97
        csp.update_domain("L5", {"min": 47, "max": 97})     # to 46, 96
        csp.update_domain("L6", {"min": 46, "max": 96})     # to 45, 95
        csp.update_domain("L7", {"min": 45, "max": 95})     # to 44, 94
        # act
        out = self.__sut.propagate(csp, {"L2"})
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[2], {"L2", "L3", "L4", "L5", "L6", "L7"})
        self.assertEqual(D["L2"], {"min": 49, "max": 99})
        self.assertEqual(D["L3"], {"min": 48, "max": 98})
        self.assertEqual(D["L4"], {"min": 47, "max": 97})
        self.assertEqual(D["L5"], {"min": 46, "max": 96})
        self.assertEqual(D["L6"], {"min": 45, "max": 95})
        self.assertEqual(D["L7"], {"min": 44, "max": 94})

    def test_establish_reduces_bounds(self):
        '''A case that all inconsistency conditions exist and are fixed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 50)
        csp.update_domain("L3", {"min": 48, "max": 50})     # to 49, 49
        csp.update_domain("L4", {"min": 47, "max": 49})     # to 48, 48
        csp.update_domain("L5", {"min": 47, "max": 47})
        csp.update_domain("L6", {"min": 45, "max": 47})     # to 46, 46
        csp.update_domain("L7", {"min": 44, "max": 46})     # to 45, 45
        # act
        out = self.__sut.establish(csp, "L2", 50)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[2], {"L3", "L4", "L6", "L7"})
        self.assertEqual(D["L3"], {"min": 49, "max": 49})
        self.assertEqual(D["L4"], {"min": 48, "max": 48})
        self.assertEqual(D["L6"], {"min": 46, "max": 46})
        self.assertEqual(D["L7"], {"min": 45, "max": 45})

    def test_establish_reduces_bounds_2(self):
        '''Another case in which inconsisten values are removed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 50)
        csp.assign("L5", 47)
        csp.update_domain("L3", {"min": 48, "max": 50})     # to 49, 49
        csp.update_domain("L4", {"min": 47, "max": 49})     # to 48, 48
        csp.update_domain("L6", {"min": 45, "max": 47})     # to 46, 46
        csp.update_domain("L7", {"min": 44, "max": 46})     # to 45, 45
        # act
        out = self.__sut.establish(csp, "L5", 47)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[2], {"L3", "L4", "L6", "L7"})
        self.assertEqual(D["L3"], {"min": 49, "max": 49})
        self.assertEqual(D["L4"], {"min": 48, "max": 48})
        self.assertEqual(D["L6"], {"min": 46, "max": 46})
        self.assertEqual(D["L7"], {"min": 45, "max": 45})

    def test_contradiction_occurs(self):
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

    def test_establish_reduces_bounds_3(self):
        '''Another case in which inconsisten values are removed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 83)
        csp.update_domain("L3", {"min": 40, "max": 100})    # to 82, 82
        csp.update_domain("L4", {"min": 40, "max": 99})     # to 81, 81
        csp.assign("L5", 80)
        csp.assign("L6", 79)
        csp.assign("L7", 78)
        # act
        out = self.__sut.establish(csp, "L5", 47)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[2], {"L3", "L4"})
        self.assertEqual(D["L3"], {"min": 82, "max": 82})
        self.assertEqual(D["L4"], {"min": 81, "max": 81})
