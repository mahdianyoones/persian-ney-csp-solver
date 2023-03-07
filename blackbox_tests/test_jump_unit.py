import unittest
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from csp import CSP
from jump import JUMP
from constants import *

class test_JUMP(unittest.TestCase):
    '''Test the behavior of jump.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = JUMP()

    def test_accumulates(self):
        '''
        Confsets:
            P2:     {P1: (1,1,1,1,10)}
            P4:     {P1: (1,1,1,1,10)}
            L7:     {P1: (1,1,1,1,10), P2: (1,1,1,1,5)}
            P3:     {P2: (1,1,1,1,5)}
            L4:     {P2: (1,1,1,1,5)}
        '''
        sut = self.__sut
        sut.accumulate("P1", (1,1,1,1,10), {"P2", "P4", "L7"})
        sut.accumulate("P2", (1,1,1,1,5), {"P3", "L4", "L7"})
        self.assertEqual(set(sut.get_confset("P2").keys()), {"P1"})
        self.assertEqual(set(sut.get_confset("P4").keys()), {"P1"})
        self.assertEqual(set(sut.get_confset("P3").keys()), {"P2"})
        self.assertEqual(set(sut.get_confset("L4").keys()), {"P2"})
        self.assertEqual(set(sut.get_confset("L7").keys()), {"P2", "P1"})

    def test_can_backjump(self):
        '''
        Confsets:
            P2:     {P1: (1,1,1,1,10)}
            P4:     {P1: (1,1,1,1,10)}
            L7:     {P1: (1,1,1,1,10), P2: (1,1,1,1,5)}
            P3:     {P2: (1,1,1,1,5)}
            L4:     {P2: (1,1,1,1,5)}
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("P1", (1,1,1,1,10))
        csp.assign("P2", (1,1,1,1,5))
        sut.accumulate("P1", 10, {"P2", "P4", "L7"})
        sut.accumulate("P2", 5, {"P3", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        self.assertFalse(sut.canbackjump("L5"))

    def test_selects_right_jump_target(self):
        '''
        Confsets:
            P2:     {P1: (1,1,1,1,10)}
            P4:     {P1: (1,1,1,1,10)}
            L7:     {P1: (1,1,1,1,10), P2: (1,1,1,1,5)}
            P3:     {P2: (1,1,1,1,5)}
            L4:     {P2: (1,1,1,1,5)}
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("P1", (1,1,1,1,10))
        csp.assign("P2", (1,1,1,1,5))
        sut.accumulate("P1", (1,1,1,1,10), {"P2", "P4", "L7"})
        sut.accumulate("P2", (1,1,1,1,5), {"P3", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        self.assertEqual(sut.jump_target(csp, "L7"), "P2")

    def test_absorbs_the_confset(self):
        '''
        Confsets:
            P1:     {L1: 1}             absrobs P2 from L7
            P4:     {P1: 10}
            L7:     {P1: (1,1,1,1,10), P2: (1,1,1,1,5)}
            P3:     {P2: 5}
            L4:     {P2: 5}
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("L1", 1)
        sut.accumulate("L1", 1, {"P1"})
        csp.assign("P1", (1,1,1,1,10))
        sut.accumulate("P1", (1,1,1,1,10), {"D5", "L7"})
        csp.assign("P2", (1,1,1,1,5))
        sut.accumulate("P2", (1,1,1,1,5), {"P3", "L4", "L7"})
        sut.absorb("P1", "L7")
        self.assertEqual(sut.get_confset("P1").keys(), {"P2", "L1"})

    def test_no_jump_to_unassigned_var(self):
        '''
        Confsets:
            P2:                     absorbs nothing from L7
            P4:     {P1: 10}
            L7:     {P2: (1,1,1,1,5)}         P2 gets unaccumulated
            P3:     {P2: (1,1,1,1,5)}         P2 gets unaccumulated
            L4:     {P2: (1,1,1,1,5)}         P2 gets unaccumulated
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("P1", (1,1,1,1,10))
        csp.assign("P2", (1,1,1,1,5))
        sut.accumulate("P1", (1,1,1,1,10), {"P4"})
        sut.accumulate("P2", (1,1,1,1,5), {"P3", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        self.assertEqual(sut.jump_target(csp, "L7"), "P2")
        sut.absorb("P2", "L7")
        csp.unassign("P2")
        A = csp.get_assignment()
        sut.unaccumulate("P2")
        self.assertFalse(sut.canbackjump("L7"))

if __name__ == "__main__":
   unittest.main()