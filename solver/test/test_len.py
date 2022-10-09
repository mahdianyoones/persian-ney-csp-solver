import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from len import LEN
from spec import specs
from constants import *

class test_LEN(unittest.TestCase):
    '''The goal is to enforce the following constraint relation:
    
        L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

        Equivalent partitions:

        L1 = len - L2 - L3 - L4 - L5 - L6 - L7
        L1 > len - L2 - L3 - L4 - L5 - L6 - L7
        L1 < len - L2 - L3 - L4 - L5 - L6 - L7

        a. A_L7 = len - A_L1 - A_L2 - A_L3 - A_L4 - A_L5 - A_L6

        a. Lower & upper are consistent.
        b. Lower & upper are inconsistent. Consistency is possible.
        c. Lower is inconsistent. Consistency Impossible.
        d. Upper is inconsistent. Consistency Impossible.
        e. One variable is examined.
        f. Two variables are examined.
        g. Seven variables are examined.

        Details:

        a) Lower & upper are consistent.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Imagine L2 to L7 are assigned their maximum values.

            min_L1 >= len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7

            Imagine L2 to L7 are assigned their minimum values.

            max_L1 <= len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7


        b) Lower & upper are inconsistent. Consistency is possible.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Imagine L2 to L7 are assigned their maximum values.

            min_L1 < len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7

            Imagine L2 to L7 are assigned their minimum values.

            max_L1 > len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7

            Consistency is made through:

            min_L1 = len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7
            max_L1 = len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7

        c) Lower is inconsistent. Consistency Impossible.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Imagine L2 to L7 are assigned their maximum values.

            min_L1 < len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7
            max_L1 < len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7

        d) Upper is inconsistent. Consistency Impossible.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Imagine L2 to L7 are assigned their maximum values.

            max_L1 > len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7
            min_L1 > len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7

        e. One variable is examined.

            1. 5 variables are assigned. Propagation occurs for one var.
            2. 5 variables are assigned. Establish occurs.

        f. Two variables are examined.

            1. 4 variables are assigned. Propagation occurs for one var.
            2. 4 variables are assigned. Establish occurs.

        g. Seven variables are examined.

            1. No variables is assigned. Propagation occurs for two variables.

    '''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = LEN(specs["C"])
    
    def __reset_csp(self):
        domain = {"min": 1, "max": 1000}
        for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            self.__csp.update_domain(var, domain)
        self.__csp.unassign_all()

    def test_all_consistent(self):
        '''Lower & upper are consistent.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Assume len = 524.

            Assume L2 to L7 are assigned their maximum values.

            min_L1 >= len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7

            8 >= 524 - 86 - 86 - 86 - 86 - 86 - 86   --->   8 >= 8

            Assume L2 to L7 are assigned their minimum values.

            max_L1 <= len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7.

            476 <= 524 - 8 - 8 - 8 - 8 - 8 - 8   --->   476 <= 476

            8 & 476 are boundary values for this partition.

            Other pairs of values such as 9/475, 10/474, and the likes fall
            into the same partition.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 8, "max": 476})
        csp.update_domain("L2", {"min": 8, "max": 476})
        csp.update_domain("L3", {"min": 8, "max": 476})
        csp.update_domain("L4", {"min": 8, "max": 476})
        csp.update_domain("L5", {"min": 8, "max": 476})
        csp.update_domain("L6", {"min": 8, "max": 476})
        csp.update_domain("L7", {"min": 8, "max": 476})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertIn("L1", output[1])

    def test_L1_reduce(self):
        ''' Lower & upper are inconsistent. Consistency is possible.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Assume len = 524.

            Assume L2 to L7 are assigned their maximum values.

            min_L1 < len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7

            Assume L2 to L7 are assigned their minimum values.

            max_L1 > len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7

            Consistency is made through:

            min_L1 = len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7
            max_L1 = len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 8, "max": 477})
        csp.update_domain("L2", {"min": 8, "max": 476})
        csp.update_domain("L3", {"min": 8, "max": 476})
        csp.update_domain("L4", {"min": 8, "max": 476})
        csp.update_domain("L5", {"min": 8, "max": 476})
        csp.update_domain("L6", {"min": 8, "max": 476})
        csp.update_domain("L7", {"min": 8, "max": 476})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertIn("L1", output[1])
        L1 = self.__csp.get_domain("L1")
        self.assertEqual(L1, {"min": 8, "max": 476})

    def test_L1_lower_contradiction(self):
        '''Lower is inconsistent. Consistency Impossible.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Assume len = 524.

            Assuming L2 to L7 are assigned their maximum values,

            min_L1 > len - max_L2 - max_L3 - max_L4 - max_L5 - max_L6 - max_L7
            
            indicates contradiction on the lower bound on L1.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 9, "max": 476})
        csp.update_domain("L2", {"min": 8, "max": 86})
        csp.update_domain("L3", {"min": 8, "max": 86})
        csp.update_domain("L4", {"min": 8, "max": 86})
        csp.update_domain("L5", {"min": 8, "max": 86})
        csp.update_domain("L6", {"min": 8, "max": 86})
        csp.update_domain("L7", {"min": 8, "max": 86})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertIn("L1", output[1])

    def test_contradiction_after_establish(self):
        '''Assers a contradictory case.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L1", 9)
        csp.assign("L2", 9)
        csp.assign("L3", 9)
        csp.assign("L4", 9)
        csp.assign("L5", 9)
        csp.assign("L6", 9)
        csp.update_domain("L7", {"min": 8, "max": 86})
        # act
        output = self.__sut.establish(csp, "L6", 9)
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"L7"})
        self.assertEqual(output[2], {"L1","L2","L3","L4","L5","L6"})

    def test_L1_upper_contradiction(self):
        '''Upper is inconsistent. Consistency Impossible.

            L1 + L2 + L3 + L4 + L5 + L6 + L7 = len

            L1 = len - L2 - L3 - L4 - L5 - L6 - L7

            Assume len = 524

            Assuming L2 to L7 are assigned their minimum values,

            max_L1 < len - min_L2 - min_L3 - min_L4 - min_L5 - min_L6 - min_L7

            475 < 476

            indicates contradiction on the upper bound of L1.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 8, "max": 475})
        csp.update_domain("L2", {"min": 8, "max": 476})
        csp.update_domain("L3", {"min": 8, "max": 476})
        csp.update_domain("L4", {"min": 8, "max": 476})
        csp.update_domain("L5", {"min": 8, "max": 476})
        csp.update_domain("L6", {"min": 8, "max": 476})
        csp.update_domain("L7", {"min": 8, "max": 476})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertIn("L1", output[1])
        
    def test_one_var_examined(self):
        '''One variable is examined.

            1. 5 variables are assigned. Propagation occurs for one var.
            2. 5 variables are assigned. Establish occurs.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L2", 10)
        csp.assign("L3", 10)
        csp.assign("L4", 10)
        csp.assign("L5", 10)
        csp.assign("L6", 10)
        # act
        output = self.__sut.establish(csp, "L7", 10)
        # assess
        self.assertEqual(output[1], {"L1"})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[1], {"L1"})
    
    def test_two_variables_examined(self):
        '''Two variables are examined.

            1. 4 variables are assigned. Propagation occurs for one var.
            2. 4 variables are assigned. Establish occurs.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.assign("L3", 10)
        csp.assign("L4", 10)
        csp.assign("L5", 10)
        csp.assign("L6", 10)
        # act
        output = self.__sut.establish(csp, "L7", 10)
        # assess
        self.assertEqual(output[1], {"L1", "L2"})
        # act
        output = self.__sut.propagate(csp, {"L7"})
        # assess
        self.assertEqual(output[1], {"L1", "L2"})

    def test_seven_variables_examined(self):
        '''Seven variables are examined.

            No variables is assigned. Propagation occurs for two variables.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        # act
        output = self.__sut.propagate(csp, {"L7", "L6"})
        # assess
        self.assertEqual(output[1], {"L1", "L2", "L3", "L4", "L5", "L6","L7"})