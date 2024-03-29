import os.path as op
from sys import path as sp
import math
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from constants import *

def get_violations(a, spec):
    violated_vars = set([])
    violated_consts = set([])
    solution_info = {}
    # half
    if not math.ceil(a["L2"] / 2) == a["L1"]:
        violated_vars.update(set(["L1", "L2"]))
        violated_consts.add("half")
    # hole 1
    if not spec["mp"]+a["L1"]+a["L2"]+a["L3"]+spec["hmarg"] < spec["h1"]:
        violated_vars.update(set(["L1", "L2", "L3"]))
        violated_consts.add("hole1")
    # hole 3    
    if not spec["mp"]+a["L1"]+a["L2"]+a["L3"]+a["L4"]+spec["hmarg"] < spec["h3"]:
        violated_vars.update(set(["L1", "L2", "L3", "L4"]))
        violated_consts.add("hole3")
    # hole 6  
    if not spec["mp"]+a["L1"]+a["L2"]+a["L3"]+a["L4"]+a["L5"]+spec["hmarg"] < spec["h6"]:
        violated_vars.update(set(["L1", "L2", "L3", "L4", "L5"]))
        violated_consts.add("hole6")
    # len
    if not spec["mp"]+a["L1"]+a["L2"]+a["L3"]+a["L4"]+a["L5"]+a["L6"]+a["L7"] == spec["len"]:
        violated_vars.update(set(["L1", "L2", "L3", "L4", "L5", "L6", "L7"]))
        violated_consts.add("len")
    # lendec lower
    for i in range(3, 7):
        Li = "L" + str(i)
        Lj = "L" + str(i-1)
        if not a[Li] >= math.floor(2/3 * a[Lj]):
            violated_vars.update(set([Li, Lj]))
            violated_consts.add("lendeclower"+str(i))
    # lendec
    for i in range(3, 8):
        Li = "L" + str(i)
        Lj = "L" + str(i-1)
        if not a[Li] < a[Lj]:
            violated_vars.update(set([Li, Lj]))
            violated_consts.add("lendec"+str(i))
    # piece min
    for i in range(1, 8):
        Pi = "P"+str(i)
        _len_Pi = a[Pi][1]
        Li = "L"+str(i)
        if not _len_Pi >= a[Li]:
            violated_vars.update(set([Li, Pi]))
            violated_consts.add("piecemin"+str(i))
    # same thick & same round
    for i in range(1, 8):
        Pi = "P"+str(i)
        for j in range(i, 8):
            Pj = "P"+str(j)
            if a[Pi][2] != a[Pj][2]:
                violated_consts.add("samethick"+str(i))
                violated_vars.update(set([Pi, Pj]))
            if a[Pi][3] != a[Pj][3]:
                violated_consts.add("sameround"+str(i))
                violated_vars.update(set([Pi, Pj]))

    return violated_vars, violated_consts

def is_valid(solution, specs):
    '''Determines whether the given solution satisfies all constraints.'''
    for s in range(0, 10000000):
        single_solution = {}
        if not "L"+str(s*7+1) in solution:
            break
        for i in range(1, 8):
            Pi = "P"+str(s*7+i)
            Li = "L"+str(s*7+i)
            single_solution["P"+str(i)] = solution[Pi]
            single_solution["L"+str(i)] = solution[Li]
        violated_vars, violated_consts = get_violations(single_solution, specs[s])
        if len(violated_consts) > 0 or len(violated_vars) > 0:
            return False
    return True