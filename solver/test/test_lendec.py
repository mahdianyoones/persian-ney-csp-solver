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
    '''The goal is to enforce the following constraint relations:
    
		L2 > L3 >= 2/3 L2
		L3 > L4 >= 2/3 L3
		L4 > L5 >= 2/3 L4
		L5 > L6 >= 2/3 L5
		L6 > L7
        
        Length of nodes decrease from top to bottom (except node 1). The
        amount of this decrement however must fall within a range.
        
        Boundary value analysis

        Illegal values:

        L3[min] < 2/3 A_L2         .
        L3[min] < 2/3 L2[min]      .
        L3[max] >= A_L2             .
        L3[max] >= L2[max]          .
        A_L6 <= L7[max]             .
        L6[max] <= L7[max]          .

        Legal values:

        L2 > L3 >= 2/3 L2   legal   .
        L6 > L7             legal   

        Contradiction cases:
        
        L3[max] < 2/3 L2[min]
        L3[max] < 2/3 A_L2
        L3[min] >= L2[min]
        L3[min] >= A_L2
        L7[min] >= L6[max]
        L7[min] >= A_L6

        '''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = LENDEC()
    
    def __reset_csp(self):
        self.__csp.unassign_all()

    def test_propagate_reduces_bounds(self):
        '''A case propagate detects and removes inconsistent values.
        
        In this case L2 changes are propagatedand L5 has legal boundaries'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L4", {"min": 90, "max": 80})
        csp.update_domain("L5", {"min": 59, "max": 80})     # to 60, 79
        csp.update_domain("L6", {"min": 39, "max": 79})     # to 40, 78
        csp.update_domain("L7", {"min": 30, "max": 78})     # to 30, 77
        # act
        out = self.__sut.propagate(csp, {"L4"})
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L5", "L6", "L7"})
        self.assertEqual(out[2], {"L5", "L6", "L7"})
        self.assertEqual(D["L5"], {"min": 60, "max": 79})
        self.assertEqual(D["L6"], {"min": 40, "max": 78})
        self.assertEqual(D["L7"], {"min": 30, "max": 77})

    def test_establish_reduces_bounds(self):
        '''A case that all inconsistency conditions exist and are fixed.
        
        In this case L2 is assigned and L5 has legal boundaries

        L3[min] < 2/3 A_L2         L3[min] must increase
        L3[max] >= A_L2            L3[max] must decrease
        L4[min] < 2/3 L3[min]      L4[min] must increase
        L4[max] >= L3[max]         L4[max] must decrease
        L5[min] >= 2/3 L4[max]     L5 remains intact
        L5[max] < L4[min]          L5 remains intact
        L6[min] >= 2/3 L5[max]     L6 remains intact
        L6[max] < L5[min]          L6 remains intact
        L6[max] <= L7[max]         L7[max] must decrease
        '''
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
        self.assertEqual(D["L7"], {"min": 13, "max": 76})

    def test_contradiction_occurs(self):
        '''A case that contradiction occurs.'''
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

    def test_contradiction_occurs_2(self):
        '''A case that contradiction occurs.'''
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