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
    '''Test the behavior of Diameter decrement constraint.

        The constraint makes sure the following relations exist between D
        variables:
    
        0.5 <= D2 - D1 <= 1.0
        0.5 <= D3 - D2 <= 1.0
        0.5 <= D4 - D3 <= 1.0
        0.5 <= D5 - D4 <= 1.0
        0.5 <= D6 - D5 <= 1.0
        0.5 <= D7 - D6 <= 1.0

        The module does one or a combination of following actions:

        - returns without any action
        - examines or does not examined variables
        - reduces or does not reduce the domain of variables
        - detects contradiction if consistency is impossible

        Contradiction occurs if one varialbe shed all its values.
        The module has two entry points: propagate and establish methods.

        propagate method is not implemeted for now; hence, only
        establish method is called.
        
        In the doc section of test cases, diff means the difference between 
        a value of one D variable and a value in the one before it, for
        example D2 - D1, D3 - D2, etc.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = DIAMDEC({"min": 0.5, "max": 1.0})
    
    def __reset_csp(self):
        self.__csp.unassign_all()

    def test_no_reduction_after_establish(self):
        '''Asserts a case that no reduction occurs.
                
            All values in the domain of all unassigned variables have one of
            these values to be considered consistent:

            diff = 1.0          a boundary value
            diff = 0.5          a boundary value
            0.5 < diff < 1.0    between the boundaries'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D2", {13})
        csp.update_domain("D3", {12.5})
        csp.update_domain("D4", {11.5})
        csp.update_domain("D5", {10.5})
        csp.update_domain("D6", {9.5})
        csp.update_domain("D7", {8.5, 8.6, 9})
        # act
        csp.assign("D1", 14)
        output = self.__sut.establish(csp, "D1", 14)
        # assess
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertEqual(output[1], {"D2","D3","D4","D5","D6","D7"})

    def test_no_reduction_after_propagation(self):
        '''Asserts a case that no reduction occurs.
                
            All values in the domain of all unassigned variables have one of
            these values to be considered consistent:

            diff = 1.0          a boundary value
            diff = 0.5          a boundary value
            0.5 < diff < 1.0    between the boundaries'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D1", {14})
        csp.update_domain("D2", {13})
        csp.update_domain("D3", {12.5})
        csp.update_domain("D4", {11.5})
        csp.update_domain("D5", {10.5})
        csp.update_domain("D6", {9.5})
        csp.update_domain("D7", {8.5, 8.6, 9})
        # act
        csp.assign("D1", 14)
        output = self.__sut.propagate(csp, {"D5", "D4", "D1", "D7"})
        # assess
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertEqual(output[1], {"D2","D3","D4","D5","D6","D7"})

    def test_reduction(self):
        '''Asserts a case in which reduction occurs.
                    
            A value must have one of these values to be considered illegal:

            diff < 0.5
            diff > 1.0'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D2", {13, 12})   # 12 is inconsistent
        csp.update_domain("D3", {12.5, 13}) # 13 is inconsistent
        csp.update_domain("D4", {11.5})
        csp.update_domain("D5", {10.5})
        csp.update_domain("D6", {9.5})
        csp.update_domain("D7", {8.4, 8.5, 8.6, 9}) # 8.4 is inconsistent
        # act
        csp.assign("D1", 14)
        output = self.__sut.establish(csp, "D1", 14)
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"D2","D3","D4","D5","D6","D7"})
        self.assertEqual(output[2], {"D2","D3","D7"})
        D = csp.get_domains()
        self.assertEqual(D["D2"], {13})     # 12 is removed
        self.assertEqual(D["D3"], {12.5})   # 12 is removed
        self.assertEqual(D["D7"], {8.5, 8.6, 9}) # 8.4 is removed

    def test_reduction_2(self):
        '''Asserts another case in which reduction happens.'''

        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D7", {5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 13})
        # act
        csp.assign("D6", 10)
        output = self.__sut.establish(csp, "D6", 10)
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"D7"})
        self.assertEqual(output[1], {"D7"})
        D = csp.get_domains()
        self.assertEqual(D["D7"], {9, 9.5})
        
    def test_contradiction(self):
        '''Asserts a contradictory case.
                    
           All values of one unassigned variables are removed.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D2", {13, 13.5, 13.6, 14})
        # act
        csp.assign("D1", 12.5)
        output = self.__sut.establish(csp, "D1", 12.5)
        # assess
        self.assertEqual(output[0], CONTRADICTION) # output indicator
        self.assertEqual(output[1], {"D2"}) # examined set
        self.assertEqual(output[2], {"D1"}) # conflict set

    def test_returns_correct_conflict_set(self):
        '''Asserts correct a conflcit set is returned.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D5", {13, 13.5, 13.6, 14})
        # act
        csp.assign("D1", 14)
        csp.assign("D2", 13)
        csp.assign("D3", 12)
        csp.assign("D4", 11)
        output = self.__sut.establish(csp, "D4", 11)
        # assess
        self.assertEqual(output[0], CONTRADICTION) # output indicator
        self.assertEqual(output[1], {"D5"}) # examined set
        self.assertEqual(output[2], {"D1","D2","D3","D4"}) # conflict set