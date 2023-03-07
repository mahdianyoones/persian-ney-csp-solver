import math
from csp import CSP
from unary import UNARY
from constants import *
from copy import copy
from mac import MAC
from spec import specs
from random import randint

def _get_violations(a, spec):
    violated_vars = set([])
    violated_consts = set([])
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

def get_violations(solution, regs, specs):
    violated_vars = set([])
    violated_consts = set([])
    for s in range(0, 10000000):
        single_solution = {}
        if not "L"+str(s*7+1) in solution:
            break
        for i in range(1, 8):
            Pi = "P"+str(s*7+i)
            Li = "L"+str(s*7+i)
            single_solution["P"+str(i)] = solution[Pi]
            single_solution["L"+str(i)] = solution[Li]
        _violated_vars, _violated_consts = _get_violations(single_solution, specs[s])
        for _violated_var in _violated_vars:
            violated_vars.add(_violated_var[0]+str(s*7+int(_violated_var[1:])))
        for _violated_const in _violated_consts:
            violated_consts.add(_violated_const+"_"+str(s))
    return violated_vars, violated_consts

def initial_assignment(csp):
    assignment = {}
    for var in csp.get_variables():
        values = csp.get_shuffled_values(var)
        assignment[var] = list(values)[randint(0, len(values) - 1)]
    return assignment

def min_conflict(mac, csp, regs, specs, max_steps = 1000):
    current_state = initial_assignment(csp)
    for i in range(0, max_steps):
        violated_vars, conflicts = get_violations(current_state, regs, specs)
        print(len(violated_vars))
        print(violated_vars)
        if violated_vars == set([]):
            return current_state
        if False:#randint(0, 1) != 0:
            best_var = None
            largest_domain_size = 0
            D = csp.get_domains()
            for var in violated_vars:
                domain_size = 0
                if var[0] == "P":
                    domain_size = len(D[var])
                else:
                    domain_size = D[var]["max"] - D[var]["min"] + 1
                if domain_size > largest_domain_size:
                    best_var = var
                    largest_domain_size = domain_size
            var = best_var
        else:
            var = list(violated_vars)[randint(0, len(violated_vars) - 1)]
        values = csp.get_shuffled_values(var)
        best_value = None
        least_conflicts = float("+inf")
        if True:#randint(0, 100) != 0:
            for val in values:
                current_state[var] = val
                violated_vars, conflicts = get_violations(current_state, regs, specs)
                if len(conflicts) < least_conflicts:
                    best_value = val
                    least_conflicts = len(conflicts)
            current_state[var] = best_value
        else:
            current_state[var] = list(values)[randint(0, len(values) - 1)]

def main():
    regs = ["Bb"]
    specs_sorted = [specs[reg] for reg in regs]
    data_set_path = "pieces.csv"
    csp = CSP(S=len(regs))
    mac = MAC()
    res = UNARY.init_domains(csp, data_set_path)
    if res == CONTRADICTION:
        print("Unary constraints are violated")
        return
    res = UNARY.unarify(csp, specs_sorted)
    if res == CONTRADICTION:
        print("Unary constraints are violated")
        return
    X = copy(csp.get_variables())
    res = mac.propagate(csp, specs_sorted, X)
    if res == CONTRADICTION:
        print("No solution could exist.")
        return
    print(min_conflict(mac, csp, regs, specs_sorted, max_steps=10000))

if __name__ == "__main__":
    main()