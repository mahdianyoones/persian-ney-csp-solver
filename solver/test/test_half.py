import unittest
import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from csp import CSP
from half import HALF
from spec import specs
from constants import *

class test_HALF(unittest.TestCase):
    '''The goal is to enforce the l1_half_l2 constraint.
    
        There must be this relation between assigned values to L1 and L2:

        L1 = L2 / 2     or      L2 = L1 * 2

        i.e. the length of first node must be half of the length of the
        second node.
        
        Note: Due to variables assignemnt order, the case that L2 is assigned
        first is not covered.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = HALF()
    
    def __reset_csp(self):
        self.__csp.unassign_all()

    def test_max_L1_min_L2_adjust(self):
        '''Asserts the case that L1 and L2 adjust due to propagation.
        
        One or two of these criteria occur:

        L1[min] > L2[min] / 2        -->     30 > 40/2
        L1[max] > L2[max] / 2        -->     40 > 70/2

        Consistency can be achieved by increasing the min of L2 and decreasing
         the max of L1.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 30, "max": 40})
        csp.update_domain("L2", {"min": 40, "max": 70})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L1", "L2"})
        self.assertEqual(out[2], {"L1", "L2"})
        D = csp.get_domains()
        self.assertEqual(D["L1"], {"min": 30, "max": 35})
        self.assertEqual(D["L2"], {"min": 60, "max": 70})

    def test_L1_assignment(self):
        '''Asserts the case that assignment to L1 causes update for L2.

        A_L1 > L2[min] / 2     andor     A_L1 < L2[max] / 2

        A_L1 = 30, L2 = {min: 59, max: 61}

        30 > 59/2   30 < 61/2'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L2", {"min": 59, "max": 61})
        csp.assign("L1", 30)
        # act
        out = self.__sut.establish(csp, "L1", 30)
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L2"})
        self.assertEqual(out[2], {"L2"})
        D = csp.get_domains()
        self.assertEqual(D["L2"], {"min": 60, "max": 60})

    def test_min_L1_max_L2_adjust(self):
        '''Asserts the case that min L1 and max L2 are inconsistent.
        
        due to partitions d and e:
        
        d. L1[min] < L2[min] / 2        -->     15 < 40/2
        e. L1[max] < L2[max] / 2        -->     30 < 70/2

        Consistency can be achieved by increasing the min of L1 and
        decreasing the max of L2.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 15, "max": 30})
        csp.update_domain("L2", {"min": 40, "max": 70})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], DOMAINS_REDUCED)
        self.assertEqual(out[1], {"L1", "L2"})
        self.assertEqual(out[2], {"L1", "L2"})
        D = csp.get_domains()
        self.assertEqual(D["L1"], {"min": 20, "max": 30})
        self.assertEqual(D["L2"], {"min": 40, "max": 60})

    def test_contradiction_occurs(self):
        '''Asserts a case that propagate catches contradiction.
        
        When the domain of both L1 and L2 are updated, and they are
        inconsistent, two cases appear: a) they can adjust b) they cannot
        
        The case a is covered by two test cases in this class. Case b occurs
        when one domain reduces to one value by another constraint. In this
        case this domain cannot adjust.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 22, "max": 22})
        csp.update_domain("L2", {"min": 40, "max": 70})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], CONTRADICTION)
        self.assertEqual(out[1], {"L1", "L2"})
    
    def test_reduced_but_consistent(self):
        '''When the domains reduced to consistent values, no update is needed.
        
        L1 reduced to (30, 50)
        L2 reduced to (60, 100)

        It is highly unlikey to happen, but the odds is not zero.
        '''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("L1", {"min": 30, "max": 50})
        csp.update_domain("L2", {"min": 60, "max": 100})
        # act
        out = self.__sut.propagate(csp, {"L1"})
        # assess
        self.assertEqual(out[0], DOMAINS_INTACT)
        self.assertEqual(out[1], {"L1", "L2"})
