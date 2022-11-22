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
    '''Test the behavior of jump.
    
    
    Upon assignment of each var: value, if contradiction occurs, we need to know
    the reason of contradiction.

    Consistency algorithms report contradiction if their participants have conflict 
    with each other. The reason of failure is the var: value pairs of participants of
    a constraint.

    Or maybe the reason of failure is the variable that's being assigned?

    For example, hole3 has three participants: L1, L2, and L3.

    If upon an assignment to L2, a contradiction occurs, L2 should be
    reported for the reason of conflict. L2 should be added to the
    conflict set 

    This is a direct reason of failure. The returned conflicting members
    
    
    Imagine, L2 gets assigned successfully,
    but its impact propagates to other variables and constraints where a
    contradiction occurs. For example, after assignment to L2, L3 gets reduced
    and MAC invokes piecemin3 where L3 is a participant. Piecemin3 reports
    contradiction but doesn't know the reason since it doesn't know what
    assignment is the origin of propagation.

    However, piecemin3 does report contradiction without any conflict set.

    '''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = JUMP()

    def test_accumulates(self):
        '''
        Confsets:

        D2:     {D1: 10}
        D4:     {D1: 10}
        L7:     {D1: 10, D2: 5}
        D3:     {D2: 5}
        T4:     {D2: 5}
        L4:     {D2: 5}
        '''
        sut = self.__sut
        sut.accumulate("D1", 10, {"D2", "D4", "L7"})
        sut.accumulate("D2", 5, {"D3", "T4", "L4", "L7"})
        self.assertEqual(sut.get_confset("D2"), {"D1": 10})
        self.assertEqual(sut.get_confset("D4"), {"D1": 10})
        self.assertEqual(sut.get_confset("D3"), {"D2": 5})
        self.assertEqual(sut.get_confset("T4"), {"D2": 5})
        self.assertEqual(sut.get_confset("L4"), {"D2": 5})
        self.assertEqual(sut.get_confset("L7"), {"D2": 5, "D1": 10})

    def test_can_backjump(self):
        '''
        Confsets:

        D2:     {D1: 10}
        D4:     {D1: 10}
        L7:     {D1: 10, D2: 5}
        D3:     {D2: 5}
        T4:     {D2: 5}
        L4:     {D2: 5}
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("D1", 10)
        csp.assign("D2", 5)
        sut.accumulate("D1", 10, {"D2", "D4", "L7"})
        sut.accumulate("D2", 5, {"D3", "T4", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        self.assertTrue(sut.canbackjump("T4"))
        self.assertFalse(sut.canbackjump("L5"))

    def test_selects_right_jump_target(self):
        '''
        Confsets:

        D2:     {D1: 10}
        D4:     {D1: 10}
        L7:     {D1: 10, D2: 5}
        D3:     {D2: 5}
        T4:     {D2: 5}
        L4:     {D2: 5}
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("D1", 10)
        csp.assign("D2", 5)
        sut.accumulate("D1", 10, {"D2", "D4", "L7"})
        sut.accumulate("D2", 5, {"D3", "T4", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        self.assertEqual(sut.jump_target(csp, "L7"), "D2")

    def test_absorbs_the_confset(self):
        '''
        Confsets:
        
        D1:     {L1: 1}             absrobs D2 from L7
        D4:     {D1: 10}
        L7:     {D1: 10, D2: 5}
        D3:     {D2: 5}
        T4:     {D2: 5}
        L4:     {D2: 5}
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("L1", 1)
        sut.accumulate("L1", 1, {"D1"})
        csp.assign("D1", 10)
        sut.accumulate("D1", 10, {"D4", "L7"})
        csp.assign("D2", 5)
        sut.accumulate("D2", 5, {"D3", "T4", "L4", "L7"})
        sut.absorb("D1", "L7")
        self.assertEqual(sut.get_confset("D1").keys(), {"D2", "L1"})

    def test_no_jump_to_unassigned_var(self):
        '''
        Confsets:

        D2:                     absorbs nothing from L7
        D4:     {D1: 10}
        L7:     {D2: 5}         D2 gets unaccumulated
        D3:     {D2: 5}         D2 gets unaccumulated
        T4:     {D2: 5}         D2 gets unaccumulated
        L4:     {D2: 5}         D2 gets unaccumulated
        '''
        sut = self.__sut
        csp = self.__csp
        csp.assign("D1", 10)
        csp.assign("D2", 5)
        sut.accumulate("D1", 10, {"D4"})
        sut.accumulate("D2", 5, {"D3", "T4", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        self.assertEqual(sut.jump_target(csp, "L7"), "D2")
        sut.absorb("D2", "L7")
        csp.unassign("D2")
        A = csp.get_assignment()
        sut.unaccumulate(A, "D2")
        self.assertFalse(sut.canbackjump("L7"))

if __name__ == "__main__":
   unittest.main()