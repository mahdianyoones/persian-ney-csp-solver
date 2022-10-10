import unittest
import sys
import os

from catalog import CATALOG
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from stock import STOCK
from spec import specs
from constants import *

class test_STOCK(unittest.TestCase):
    '''The goal is to enforce the stock constraints.
    
    There are 7 similar constraints for 7 groups of variables. stock1 to 
    stock7 for T1, R1, and D1 through T7, R7, and D7 respectively.

    If D1 = 18 and T1 & R1 are unassigned, stock1 consistency reduces T1 and
    R1 to thickness and roundness of the pieces that have diameter 18.

    If D1 = 18 and T1 = 2 & R1 is unassigned, stock1 consistency reduces R1
    to roundness values of the pieces that have diameter 18 and thickness 2.

    stock2 through stock7 constraints perform the same.

    Partitions:

    a. D, T, and R are assigned
        
        L should reduce

    b. D and T are assigned

        R and L should reduce

    c. D is assigned

        R, T, and L should reduce

    d. No variable is assigned

        No examination and no reduction
        
    e. New L is out of range'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__catalog = CATALOG()
        self.__catalog.setup()
        self.__catalog.add_piece(1, 18, 0, 10) # (T, D, R, L)
        self.__catalog.add_piece(1, 19, 0, 10)
        self.__catalog.add_piece(1, 19, 0, 10)
        self.__catalog.add_piece(2, 19, 1, 10)
        self.__catalog.add_piece(2, 19, 0, 10)
        self.__catalog.add_piece(3, 20, 2, 10)
        self.__sut = STOCK(self.__catalog)
    
    def __reset_csp(self):
        csp = self.__csp
        csp.unassign_all()
        # node 1
        csp.update_domain("T1", {1, 2, 3})
        csp.update_domain("D1", {18, 19, 20})
        csp.update_domain("R1", {0, 1, 2})
        csp.update_domain("L1", {"min": 1, "max": 1000}) # arbitrary upper
        # node 2
        csp.update_domain("T2", {1, 2, 3})
        csp.update_domain("D2", {18, 19, 20})
        csp.update_domain("R2", {0, 1, 2})
        csp.update_domain("L2", {"min": 1, "max": 1000}) # arbitrary upper

    def test_L_reduces(self):
        '''Asserts a case that with D1, R1, and T1 assignments, L1 reduce.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("T1", 1)
        csp.assign("D1", 19)
        csp.assign("R1", 0)
        # act
        out = self.__sut.establish(csp, "T1", 1)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L1"})
        self.assertEqual(out[2], {"L1"})
        self.assertEqual(D["L1"], {"min": 1, "max": 20})

    def test_L_reduces_2(self):
        '''Asserts a case that with D2, R2, and T2 assignments, L2 reduce.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("T2", 1)
        csp.assign("D2", 18)
        csp.assign("R2", 0)
        # act
        out = self.__sut.establish(csp, "T2", 1)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L2"})
        self.assertEqual(out[2], {"L2"})
        self.assertEqual(D["L2"], {"min": 1, "max": 10})

    def test_contradiction_occurs(self):
        '''Asserts a case L1 reduce below its lower bound.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("D1", 19)
        csp.assign("R1", 0)
        csp.assign("T1", 1)
        csp.update_domain("L1", {"min": 21, "max": 100}) # arbitrary upper
        # act
        out = self.__sut.establish(csp, "T1", 1)
        # assess
        D = csp.get_domains()
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L1"})
        self.assertEqual(out[2], {"D1", "R1", "T1"})

    def test_LT_reduce(self):
        '''Asserts a case that L1 and T1 are reduced.
        
        Assigning R1 and D1 limits the choices for T1 and L1.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("D1", 19)
        csp.assign("R1", 0)
        # act
        out = self.__sut.establish(csp, "R1", 0)
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"T1", "L1"})
        self.assertEqual(out[2], {"T1", "L1"})
        D = csp.get_domains()
        self.assertEqual(D["T1"], {1, 2})
        self.assertEqual(D["L1"], {"min": 1, "max": 30})

    def test_LTD_reduce(self):
        '''Asserts a case that L1, T1, and D1 are reduced.
        
        Assigning R1 limits the choices for T1, D1, and L1.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("R1", 0)
        # act
        out = self.__sut.establish(csp, "R1", 0)
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"D1", "T1", "L1"})
        self.assertEqual(out[2], {"D1", "T1", "L1"})
        D = csp.get_domains()
        self.assertEqual(D["T1"], {1, 2})
        self.assertEqual(D["D1"], {18, 19})
        self.assertEqual(D["L1"], {"min": 1, "max": 40})

    def test_no_reduction(self):
        '''Asserts a case that no assignment impacts nothing.
        
        When no variable is assigned, no variable is limited.
        '''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        # act
        out = self.__sut.propagate(csp, {"R1"})
        # assess
        self.assertEqual(out[0], DOMAIN_INTACT)
        self.assertEqual(out[1], set([]))