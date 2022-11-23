import copy
from hole1 import HOLE1
from hole3 import HOLE3
from hole6 import HOLE6
from len import LEN
from lendec import LENDEC
from lendec_lower import LENDEC_LOWER
from diamdec import DIAMDEC
from samethick import SAMETHICK
from sameround import SAMEROUND
from half import HALF
from stock import THICK_STOCK, DIAM_STOCK, PIECE_STOCK, ROUND_STOCK
from piecemin import PIECEMIN
from piecemax import PIECEMAX
from constants import *

class MAC():
    '''Implements MAC for binary and higher constraints.'''

    def __init__(self, csp, catalog, spec):
        self.__csp = csp
        self.__catalog = catalog
        self.__X2C = {}
        self.__constraints_order = {}
        self.__init_c_order(csp)
        self.__init_X2C(csp)
        self.__refs = {
            "hole1":		HOLE1(spec["h1"], spec["hmarg"]),
            "hole3":		HOLE3(spec["h3"], spec["hmarg"]),
            "hole6":		HOLE6(spec["h6"], spec["hmarg"]),
            "half":			HALF(),
            "samethick":	SAMETHICK(),
            "sameround":	SAMEROUND(),
            "len":			LEN(spec["len"])
        }
        self.__pstockref = PIECE_STOCK(self.__catalog)
        self.__rstockref = ROUND_STOCK(self.__catalog)
        self.__dstockref = DIAM_STOCK(self.__catalog)
        self.__tstockref = THICK_STOCK(self.__catalog)
        self.__pieceminref = PIECEMIN()
        self.__piecemaxref = PIECEMAX()
        self.__diamdecref = DIAMDEC(spec["ddiff"])
        self.__lendecref = LENDEC()
        self.__llref = LENDEC_LOWER()
        for i in range(1, 8):
            self.__refs["pstock"+str(i)] = self.__pstockref
            self.__refs["rstock"+str(i)] = self.__rstockref
            self.__refs["dstock"+str(i)] = self.__dstockref
            self.__refs["tstock"+str(i)] = self.__tstockref
            self.__refs["piecemin"+str(i)] = self.__pieceminref
            self.__refs["nodemax"+str(i)] = self.__piecemaxref
            if i < 7:
                self.__refs["diamdec"+str(i)] = self.__diamdecref
            if i >= 2 and i < 7:
                self.__refs["lendec"+str(i)] = self.__lendecref
                self.__refs["lendeclower"+str(i)] = self.__llref

    def establish(self, curvar, value):
        '''Establishes consistency after var: value assignment.
        
        Calls all the consistency algorithms of the constraints on curvar.

        The effect of domain reductions is then kept in check by the
        upper subroutine calling the propagate method.
        
        Constraints that may have bigger impacts are called first.'''
        csp = self.__csp
        unassigned_vars = csp.get_unassigned_vars()
        constraints = self.__X2C[curvar]
        reduced_vars = set([])
        for const in constraints:
            parts = csp.get_neighbors(const)
            unassigned_parts = parts.intersection(unassigned_vars)
            if unassigned_parts == set([]):
                continue
            result = self.__refs[const].establish(csp, curvar, value, parts)
            if result[0] == CONTRADICTION:
                return result
            elif isinstance(result, tuple) and result[0] == MADE_CONSISTENT:
                reduced_vars.update(result[1])
        if len(reduced_vars) > 0:
            result = self.propagate(copy.copy(reduced_vars))
            if result[0] == CONTRADICTION:
                return result
            elif isinstance(result, tuple) and result[0] == MADE_CONSISTENT:
                reduced_vars.update(result[1])
        if len(reduced_vars) > 0:
            return (MADE_CONSISTENT, reduced_vars)
        return ALREADY_CONSISTENT

    def propagate(self, reduced_vars):
        '''Recursively propagates domain reductions.'''
        csp = self.__csp
        new_reduced_vars = set([])
        unassigned_vars = csp.get_unassigned_vars()
        while len(reduced_vars) > 0:
            _var = reduced_vars.pop()
            constraints = self.__X2C[_var]
            for constraint in constraints:
                parts = csp.get_neighbors(constraint)
                if parts.intersection(unassigned_vars) == set([]):
                    continue
                reduced_prtcns = reduced_vars.intersection(parts)
                reduced_prtcns.add(_var)
                res = self.__refs[constraint].propagate(csp, reduced_prtcns, parts)
                if res[0] == CONTRADICTION:
                    return res
                elif isinstance(res, tuple) and res[0] == MADE_CONSISTENT:
                    new_reduced_vars.update(res[1])
                    reduced_vars.update(res[1])
        if len(new_reduced_vars) > 0:
            return (MADE_CONSISTENT, new_reduced_vars)
        return ALREADY_CONSISTENT
    
    def __init_c_order(self, csp):
        '''Determines the order of constraints.
        
        A constraint order denotes the number of participants it has.'''
        constraints = csp.get_constraints()
        for constraint, participants in constraints.items():
            self.__constraints_order[constraint] = 8 - len(participants)

    def __init_X2C(self, csp):
        '''Buils a map from each variable to the constraints they participate.
        
        Constraints of each variable are sorted based on their order.'''
        C = csp.get_constraints()
        X = csp.get_variables()
        X2C = {}
        corders = self.__constraints_order
        for constraint, _vars in C.items():
            for v in X:
                if not v in X2C:
                    X2C[v] = set([])
                if v in _vars:
                    X2C[v].add(constraint)
        for v, constraints in X2C.items():
            self.__X2C[v] = sorted(constraints, key=lambda c: corders[c])