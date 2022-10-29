import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from lendec_lower import LENDEC_LOWER
from spec import specs
from constants import *

class test_LENDEC_LOWER(unittest.TestCase):
    '''Tests the behavior of len decrement consistency.
    
    The following inequalities are established between variables L2 to L6:

    L3 >= 2/3 L2

    L4 >= 2/3 L3

    L5 >= 2/3 L4

    L6 >= 2/3 L5'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = LENDEC_LOWER()
    
    def __reset_csp(self):
        self.__csp.unassign_all()

    def test_establish_reduces_bounds(self):
        '''A case in which propagate detects and removes inconsistent values.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 121)
        csp.assign("L3", 90)
        csp.update_domain("L4", {"min": 59, "max": 89})     # to 60, 89
        csp.update_domain("L5", {"min": 39, "max": 88})     # to 40, 88
        csp.update_domain("L6", {"min": 35, "max": 87})
        # act
        out = self.__sut.establish(csp, "L3", 90)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[2], {"L4", "L5"})
        self.assertEqual(D["L4"], {"min": 60, "max": 89})
        self.assertEqual(D["L5"], {"min": 40, "max": 88})

    def test_bug1212(self):
        '''A case in which propagate detects and removes inconsistent values.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L2", {"min": 90, "max": 172}) # examined, intact
        csp.update_domain("L3", {"min": 89, "max": 171}) # examined, intact
        csp.update_domain("L4", {"min": 88, "max": 170}) # examined, intact
        csp.update_domain("L5", {"min": 87, "max": 169}) # examined, intact
        csp.update_domain("L6", {"min": 30, "max": 248}) # reduced
        # act
        out = self.__sut.propagate(csp, {"L2","L3","L4","L5","L6"})
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L2","L3","L4","L5","L6"})
        self.assertEqual(out[2], {"L6"})
        self.assertEqual(D["L6"], {"min": 58, "max": 248})

    def test_contradiction_occurs(self):
        '''A case in which contradiction occurs.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 90)
        csp.update_domain("L3", {"min": 1, "max": 59}) # min cannot become 60
       # act
        out = self.__sut.establish(csp, "L2", 90)
        # assess
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[2], {"L2"})