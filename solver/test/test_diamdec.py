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
    '''The goal is to enforce the following constraint relations:
    
        0.5 <= D2 - D1 <= 1
        0.5 <= D3 - D2 <= 1
        0.5 <= D4 - D3 <= 1
        0.5 <= D5 - D4 <= 1
        0.5 <= D6 - D5 <= 1
        0.5 <= D7 - D6 <= 1

        i.e. the diamater difference between adjacent nodes must 
        fall into a range.

        - Boundary value analysis -

        Given the above criteria, the constraint behavior for D1/D2
        is as follows:

        D2 - D1 = 0.5       --->   Keeps the value of D2
        D2 - D1 = 1         --->   Keeps the value of D2
        0.5 < D2 - D1 < 1   --->   Keeps the value of D2
        D2 - D1 < 0.5       --->   Removes the value of D2
        D2 - D1 > 1         --->   Removes the value of D2

        The above cases occur in comparing each value of D1 with each value of
        D2.

        When every value of D1 is compared against every value of D2 and
        possible removals are done, three distinct cases occur:

        1. No value from D2 is removed.
        2. Some value from D2 are removed.
        3. All values from D2 are removed.

        In case 3, the algorithm stops and returns CONTRADICTION; i.e. it does
        not continue comparing D2/D3 and so forth in vain.

        In case 1 also, the algorithm stops and returns DOMAINS_INTACT; i.e.
        it does not comparing D2/D3 and so forth in vain.

        In case 2, further pairs of variables are examined and made
        consistent. At any point, if the domain of a variable is exhausted,
        CONTRADICTION is occured.

        Note that the algorithm returns the list of examined variables
        in addition to the result indicator (e.g. CONTRADICTION).

        The same behavior is repeated for D2/D3, D3/D4, ... and D6/D7.

        Equivalence partitions:

        a. No reduction happens
        
            One or a combination of these criteria happen:

            D2 - D1 = 0.5, 
            D2 - D1 = 1, 
            0.5 < D2 - D1 < 1

            D1 = {14, 14.5}       D2 = {13.5}     D3 = {13}      D4 = {12.5}
            D5 = {11.5}     D6 = {10.6}     D7 = {10.1}

            Examined:  {D2}
            Indicator: DOMAINS_INTACT

            This also case covers the case that the algorithm does not continue
            comparing further pairs in vain if no reduction happens at 
            a point.

        b. Domains reduce

            One or a combination of these criteria happen:

            D2 - D1 < 0.5,
            D2 - D1 > 1

            D1 = {13, 14}       D2 = {13.6, 13.5}  D3 = {13, 13.1}   D4 = {12.5}
            D5 = {11.5, 11.4}     D6 = {10.6}     D7 = {10.1}

            Examined:  {D1, D2, D3, D4, D5, D6}
            Indicator: DOMAINS_REDUCED
            Post-conditions:
            D1 = {14}       D2 = {13.5}     D3 = {13}      D4 = {12.5}   
            D5 = {11.5}     D6 = {10.6}     D7 = {10.1}

            This also case covers the case that the algorithm does not continue
            comparing further pairs in vain if no reduction happens at 
            a point. It stops at D6.

        c. Contradiction

            One or a combination of these criteria happen:

            D2 - D1 < 0.5,
            D2 - D1 > 1

            D1 = {14}       D2 = {13.6, 13.5}  D3 = {13, 13.1}   D4 = {12.5}
            D5 = {11.5, 11.4}     D6 = {10.6}     D7 = {9}

            Examined:  {D2, D3, D4, D5, D6, D7}
            Indicator: CONTRADICTION

            The only value of D7 is removed and contradiction occurs.
        
        d. Does not examine further variable pairs in vain

            One or a combination of these criteria happen:

            D2 - D1 < 0.5,
            D2 - D1 > 1

            D1 = {14}       D2 = {13.6}  D3 = {13, 13.1}   D4 = {12.5}
            D5 = {11.5, 11.4}     D6 = {10.6}     D7 = {9}

            Examined:  {D2}
            Indicator: CONTRADICTION

            The only value of D2 is removed and contradiction occurs.

        e. Checks due to establish occur in one direction only (Should it?)

            D1 = {14}            D2 = {13.4}    D3 = {13, 13.1}    D4 = {12.5}
            D5 = {11.5, 11.4}    D6 = {10.6}    D7 = {9}
            
            establish(D5, 11.4)

            Examined:  {D6, D7}
            Indicator: CONTRADICTION

            In this case, D5 is being assigned a value. Other variables
            need to be kept in check in this constraint. However,
            because of the nature of the constraint, variables with higher

        e. All vars are examined due to propagate

            D1 = {14}            D2 = {13.4}    D3 = {13, 13.1}    D4 = {12.5}
            D5 = {11.4}    D6 = {10.6}    D7 = {9}
            
            assign(D1, 14)
            assign(D2, 13.4)
            propagate(D5)

            Examined:  {D3, D4, D5}
            Indicator: CONTRADICTION

            If any variable loses some value in another palce, a con

        Note: At first, the values are not consistent. When D1 is assigned,
        consistency is established. And from that point onward, the values are
        always consistent. That's why the algorithm does not continue checking
        values of further variables if no reduction occurs for one variable.
    '''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = LEN(specs["C"])
    
    def __reset_csp(self):
        domain = {"min": 1, "max": 1000}
        for var in {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}:
            self.__csp.update_domain(var, domain)
        self.__csp.unassign_all()
