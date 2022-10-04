import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from diamdec import DIAMDEC
from spec import specs
from constants import *

class test_DIAMDEC(unittest.TestCase):
    '''The goal is to enforce the following constraint relations:
    
        A:

        0.5 <= D2 - D1 <= 1
        0.5 <= D3 - D2 <= 1
        0.5 <= D4 - D3 <= 1
        0.5 <= D5 - D4 <= 1
        0.5 <= D6 - D5 <= 1
        0.5 <= D7 - D6 <= 1

        i.e. the diamater difference between adjacent nodes must 
        fall into an accepted range.

        Partitions:

        a. Di - D_i-1 = 0.5                         within range
        b. Di - D_i-1 = 1                           within range
        c. 0.5 < Di - D_i-1 < 1                     within range
        d. Di - D_i-1 < 0.5                         out of range
        e. Di - D_i-1 > 1                           out of range
        f. Some values in D1 are illegal            removal from D1
        h. No variable shed values                  DOMAINS_INTACT
        i. Some variables shed values               DOMAINS_REDUCED
        j. One variable shed all its values         CONTRADICTION'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = DIAMDEC({"min": 0.5, "max": 1.0})
    
    def __reset_csp(self):
        self.__csp.unassign_all()

    def test_contradiction_occurs(self):
        '''Asserts a contradictory case.
                    
            One of these criteria must hold true for a value to be illegal:

            Di - D_i-1 < 0.5
            Di - D_i-1 > 1'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D2", {13, 13.5, 13.6, 14})
        # act
        csp.assign("D1", 12.5)
        output = self.__sut.establish(csp, "D1", 12.5)
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"D2"})

    def test_reduction_occurs(self):
        '''Asserts a case in which reduction happens.
                    
            One of these criteria must hold true for a value to be illegal:

            Di - D_i-1 < 0.5
            Di - D_i-1 > 1
            
            This case also covers the partition that no legal values in D2
            is found for a value in D1.

            For which, consistency is achieved by removing the value from D1.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D2", {13, 13.5, 13.6, 14})
        csp.update_domain("D3", {11, 12, 12.5, 13, 13.5})
        csp.update_domain("D4", {11, 11.5, 12, 12.5, 13})
        csp.update_domain("D5", {10, 10.5, 11, 11.5, 12, 12.5})
        csp.update_domain("D6", {8, 9, 9.5, 10, 10.5, 11, 11.5, 12})
        csp.update_domain("D7", {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13})
        # act
        csp.assign("D1", 14)
        output = self.__sut.establish(csp, "D1", 14)
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"D2","D3","D4","D5","D6","D7"})
        self.assertEqual(output[1], {"D2","D3","D4","D5","D6","D7"})
        D = csp.get_domains()
        self.assertEqual(D["D2"], {13, 13.5})
        self.assertEqual(D["D3"], {12, 12.5, 13})
        self.assertEqual(D["D4"], {11, 11.5, 12, 12.5})
        self.assertEqual(D["D5"], {10, 10.5, 11, 11.5, 12})
        self.assertEqual(D["D6"], {9, 9.5, 10, 10.5, 11, 11.5})
        self.assertEqual(D["D7"], {8, 8.5, 9, 9.5, 10, 10.5, 11})

    def test_reduction_occurs_2(self):
        '''Asserts a case in which reduction happens.
                    
            One of these criteria must hold true for a value to be illegal:

            Di - D_i-1 < 0.5
            Di - D_i-1 > 1
            
            This case also covers the partition that no legal values in D2
            is found for a value in D1.

            For which, consistency is achieved by removing the value from D1.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D7", {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13})
        # act
        csp.assign("D1", 14)
        output = self.__sut.establish(csp, "D6", 10)
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"D7"})
        self.assertEqual(output[1], {"D7"})
        D = csp.get_domains()
        self.assertEqual(D["D7"], {9, 9.5})

    def test_no_reduction(self):
        '''Asserts a case that no reduction occurs.
                
            One of these criteria must hold true for a value to be legal:

            Di - D_i-1 = 0.5
            Di - D_i-1 = 1
            0.5 < Di - D_i-1 < 1'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D2", {13, 13.5})
        csp.update_domain("D3", {12, 12.5, 13})
        csp.update_domain("D4", {11, 11.5, 12, 12.5})
        csp.update_domain("D5", {10, 10.5, 11, 11.5, 12})
        csp.update_domain("D6", {9, 9.5, 10, 10.5, 11, 11.5})
        csp.update_domain("D7", {8, 8.5, 9, 9.5, 10, 10.5, 11})
        # act
        csp.assign("D1", 14)
        output = self.__sut.establish(csp, "D1", 14)

        # assess
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertEqual(output[1], {"D2","D3","D4","D5","D6","D7"})
        D = csp.get_domains()