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
    '''Tests the behavior of len decrement consistency.'''
    
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
        csp.update_domain("L4", {"min": 90, "max": 80})
        csp.update_domain("L5", {"min": 59, "max": 80})     # to 60, 79
        csp.update_domain("L6", {"min": 39, "max": 79})     # to 40, 78
        csp.update_domain("L7", {"min": 39, "max": 78})     # to 39, 77
        # act
        out = self.__sut.propagate(csp, {"L4", "L6", "L7"})
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L5", "L6", "L7"})
        self.assertEqual(out[2], {"L5", "L6", "L7"})
        self.assertEqual(D["L5"], {"min": 60, "max": 79})
        self.assertEqual(D["L6"], {"min": 40, "max": 78})
        self.assertEqual(D["L7"], {"min": 39, "max": 77})

    def test_establish_reduces_bounds(self):
        '''A case that all inconsistency conditions exist and are fixed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L3", {"min": 53, "max": 81})    # to 54, 80
        csp.update_domain("L4", {"min": 35, "max": 80})    # to 36, 79
        csp.update_domain("L5", {"min": 24, "max": 78})
        csp.update_domain("L6", {"min": 15, "max": 77})    # to 16, 77
        csp.update_domain("L7", {"min": 13, "max": 77})    # to 13, 76
        # act
        csp.assign("L2", 81)
        out = self.__sut.establish(csp, "L2", 81)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L3", "L4", "L5", "L6", "L7"})
        self.assertEqual(out[2], {"L3", "L4", "L6", "L7"})
        self.assertEqual(D["L3"], {"min": 54, "max": 80})
        self.assertEqual(D["L4"], {"min": 36, "max": 79})
        self.assertEqual(D["L6"], {"min": 16, "max": 77})
        self.assertEqual(D["L7"], {"min": 15, "max": 76})

    def test_establish_reduces_bounds_2(self):
        '''Another case in which inconsisten values are removed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 81)
        csp.update_domain("L3", {"min": 53, "max": 81})    # to 54, 80
        csp.assign("L4", 36)
        csp.update_domain("L5", {"min": 23, "max": 36})    # to 24, 35
        csp.assign("L6", 18)
        csp.update_domain("L7", {"min": 16, "max": 18})    # to 17, 17
        # act
        out = self.__sut.establish(csp, "L2", 81)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L3", "L5", "L7"})
        self.assertEqual(out[2], {"L3", "L5", "L7"})
        self.assertEqual(D["L3"], {"min": 54, "max": 80})
        self.assertEqual(D["L5"], {"min": 24, "max": 35})
        self.assertEqual(D["L7"], {"min": 17, "max": 17})

    def test_contradiction_occurs(self):
        '''A case in which contradiction occurs.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L3", {"min": 53, "max": 53}) # min cannot become 54
       # act
        csp.assign("L2", 81)
        out = self.__sut.establish(csp, "L2", 81)
        # assess
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L3"})
        self.assertEqual(out[2], {"L2"})

    def test_contradiction_occurs_2(self):
        '''Another case in which contradiction occurs.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L3", {"min": 54, "max": 80})
        csp.update_domain("L4", {"min": 36, "max": 79})
        csp.update_domain("L5", {"min": 24, "max": 78})
        csp.update_domain("L6", {"min": 16, "max": 77})
        csp.update_domain("L7", {"min": 16, "max": 76})
        # act
        csp.assign("L2", 81)
        out = self.__sut.establish(csp, "L2", 81)
        # assess
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L3", "L4", "L5", "L6", "L7"})