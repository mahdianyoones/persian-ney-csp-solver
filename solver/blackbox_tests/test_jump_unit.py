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
        sut = self.__sut
        csp = self.__csp
        csp.assign("D1", 10)
        csp.assign("D2", 5)
        sut.accumulate("D1", 10, {"D2", "D4", "L7"})
        sut.accumulate("D2", 5, {"D3", "T4", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        jump_target = sut.jump_target(csp, "L7")
        self.assertEqual(jump_target, "D2")

    def test_absorbs_the_confset(self):
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
        sut = self.__sut
        csp = self.__csp
        csp.assign("D1", 10)
        csp.assign("D2", 5)
        sut.accumulate("D1", 10, {"D4"})
        sut.accumulate("D2", 5, {"D3", "T4", "L4", "L7"})
        self.assertTrue(sut.canbackjump("L7"))
        jump_target = sut.jump_target(csp, "L7")
        self.assertEqual(jump_target, "D2")
        sut.absorb("D2", "L7")
        csp.unassign("D2")
        A = csp.get_assignment()
        sut.unaccumulate(A, "D2")
        csp.assign("D2", 6)
        self.assertFalse(sut.canbackjump("L7"))

if __name__ == "__main__":
   unittest.main()