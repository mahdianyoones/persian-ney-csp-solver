import os.path as op
from sys import path as sp
import math
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from spec import specs
from constants import *

def get_violations(a, catalog, kook = None):
    violated_vars = []
    violated_consts = set([])
    spec = specs[kook]
    # half
    if not math.ceil(a["L2"] / 2) == a["L1"]:
        violated_vars.extend(["L1", "L2"])
        violated_consts.add("half")
    # hole 1
    if not a["L1"]+a["L2"]+a["L3"]+spec["hmarg"] < spec["h1"]:
        violated_vars.extend(["L1", "L2", "L3"])
        violated_consts.add("hole1")
    # hole 3    
    if not a["L1"]+a["L2"]+a["L3"]+a["L4"]+spec["hmarg"] < spec["h3"]:
        violated_vars.extend(["L1", "L2", "L3", "L4"])
        violated_consts.add("hole3")
    # hole 6  
    if not a["L1"]+a["L2"]+a["L3"]+a["L4"]+a["L5"]+spec["hmarg"] < spec["h6"]:
        violated_vars.extend(["L1", "L2", "L3", "L4", "L5"])
        violated_consts.add("hole6")
    # len
    if not a["L1"]+a["L2"]+a["L3"]+a["L4"]+a["L5"]+a["L6"]+a["L7"] == spec["len"]:
        violated_vars.extend(["L1", "L2", "L3", "L4", "L5", "L6", "L7"])
        violated_consts.add("len")
    # lendec lower
    for i in range(3, 7):
        Li = "L" + str(i)
        Lj = "L" + str(i-1)
        if not a[Li] >= math.floor(2/3 * a[Lj]):
            violated_vars.extend([Li, Lj])
            violated_consts.add("lendeclower"+str(i))
    # lendec
    for i in range(3, 8):
        Li = "L" + str(i)
        Lj = "L" + str(i-1)
        if not a[Li] < a[Lj]:
            violated_vars.extend([Li, Lj])
            violated_consts.add("lendec"+str(i))
    # piece min
    for i in range(1, 8):
        Pi = "P"+str(i)
        no, _len_Pi = a[Pi]
        Li = "L"+str(i)
        if not _len_Pi >= a[Li]:
            violated_vars.extend([Li, Pi])
            violated_consts.add("piecemin"+str(i))
    # same thick & same round
    for i in range(1, 8):
        Ti = "T"+str(i)
        Ri = "R"+str(i)
        for j in range(i, 8):
            Tj = "T"+str(j)
            Rj = "R"+str(j)
            if not a[Ti] == a[Tj]:
                violated_consts.add("samethick"+str(i))
                violated_vars.extend([Ti, Tj])
            if not a[Ri] == a[Rj]:
                violated_consts.add("sameround"+str(i))
                violated_vars.extend([Ri, Rj])
    for i in range(1, 8):
        Di = "D"+str(i)
        Ti = "D"+str(i)
        Ri = "D"+str(i)
        filters = {key[0]: a[key] for key in {Di, Ri, Ti}}
        found_pieces = catalog.pieces(filters)
        if not len(found_pieces) > 0:
            violated_vars.extend([Ri, Ti, Di])
            violated_consts.add("stock"+str(i))
    return violated_vars, violated_consts

def is_valid(solution, catalog, kook):
    '''Determines whether the given solution satisfies all constraints.'''
    violated_vars, violated_consts = get_violations(solution, catalog, kook=kook)
    return len(violated_consts) == 0 and len(violated_vars) == 0