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
        fall into an accepted range.

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

        Note that the algorithm returns the list of examined variables
        in addition to the result indicator (e.g. CONTRADICTION).

        The same behavior is repeated for D2/D3, D3/D4, ... and D6/D7.

        The algorithm checks all values in case D1 is being propagated. 
        The reason is that all domains must once become consistent
        for the algorithm to work correctly. This is also for effociency 
        reasons. With this assumption, the algorithm can always terminate
        quickly when reduction does not happen. Think of so many times that
        propagate and establish are invoked. We don't need to 
        always check all variables.

        In other cases, the algorithm stops checking further variables in case
        either contradiction or no reduction occur.

        Note: At first D1 is propagated to make all variables consistent. 
        From that point onward, the values are always consistent. That's why
        the algorithm does not continue checking values of further 
        variables if no reduction occurs.'''
    
    def setUp(self):
        self.__csp = CSP()
        self.__sut = DIAMDEC(specs["ddiff"])
    
    def __reset_csp(self):
        self.__csp.unassign_all()

    def test_no_reduction(self):
        '''Asserts a case that no reduction happens.
        
            i.e. All values are legal!
            
            One or a combination of these criteria must hold true:

            D2 - D1 = 0.5, 
            D2 - D1 = 1, 
            0.5 < D2 - D1 < 1
            
            This case also covers the case that no further variables are 
            examined in case all values of a variable are legal.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D1", {14.5})
        csp.update_domain("D2", {13.5})
        csp.update_domain("D3", {13})
        csp.update_domain("D4", {12.5})
        csp.update_domain("D5", {11.5, 11.6})
        csp.update_domain("D6", {10.6})
        csp.update_domain("D7", {10.1})
        # act
        output = self.__sut.establish("D1", 14.5)
        # assess
        self.assertEqual(output[0], DOMAINS_INTACT)
        self.assertEqual(output[1], {"D2"})

    def test_domains_reduce(self):
        '''Asserts a case that domains reduce.

            Illegal values satisfy one of these criteria:

            D2 - D1 < 0.5,
            D2 - D1 > 1.
            
            When propagation occurs for D1, all variables are examined.
            Otherwise, no further variables are examined in case no
            reduction occurs.
            
            This is to make sure that initially all values are legal.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D1", {13, 14})
        csp.update_domain("D2", {13.5, 13.6})
        csp.update_domain("D3", {13, 13.1})
        csp.update_domain("D4", {12.5})
        csp.update_domain("D5", {11.5, 11.4})
        csp.update_domain("D6", {10.6})
        csp.update_domain("D7", {10.1})
        # act
        output = self.__sut.propagate("D1")
        # assess
        self.assertEqual(output[0], DOMAINS_REDUCED)
        self.assertEqual(output[1], {"D1","D2","D3","D4","D5","D6","D7"})
        D = csp.get_domains()
        self.assertEqual(D["D1"], {14})
        self.assertEqual(D["D2"], {13.5, 13.6})
        self.assertEqual(D["D3"], {13, 13.1})
        self.assertEqual(D["D4"], {12.5})
        self.assertEqual(D["D5"], {11.5})
        self.assertEqual(D["D6"], {10.6})
        self.assertEqual(D["D7"], {10.1})
        
    def test_contradiction(self):
        '''Asserts a case that contradiction occurs.

            If a domain sheds all its values, contradiction is occured.

            D2 - D1 < 0.5,
            D2 - D1 > 1

            This case also covers the case that further variables aren't
            examined in case contradiction is detected.
            '''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D1", {13, 14})
        csp.update_domain("D2", {13.5, 13.6})
        csp.update_domain("D3", {13, 13.1})
        csp.update_domain("D4", {12.5})
        csp.update_domain("D5", {11.5, 11.4})
        csp.update_domain("D6", {9})
        csp.update_domain("D7", {8.5})
        # act
        output = self.__sut.propagate("D1")
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"D1","D2","D3","D4","D5","D6"})

    def test_examines_in_one_direction(self):
        '''Asserts that examination occurs in one direction only.

            D1 = {14}            D2 = {13.4}    D3 = {13, 13.1}    D4 = {12.5}
            D5 = {11.6, 11.5}    D6 = {10.5}    D7 = {9}
            
            establish(D5, 11.6) /or/ remove 11.5 from D5 & invoke propagate(D5)

            Examined:  {D6, D7}
            Indicator: CONTRADICTION

            0.5 <= D6 - D5 <= 1 will be violated   -->  1.1 > 1

            Why this behavior matters?

            For efficiency. The values of each variable are examined against 
            its previous variable. For example, if D5 sheds a value, first D5
            itself still contains consistent values (only one legal value 
            has been removed), and second some values of D6 might get their
            legality from the removed value from D5. If this insident renders
            some values of D6 illegal, removal of which, in turn, might render
            some values of D7 illegal too. In general, dependencies are 
            backward, not forward. That is D4 does not depend on D5, but D6 
            depends on D5, D5 does not depend on D6, but D6 depends on D5, and
            so forth.'''
        # arrange
        self.__reset_csp()
        csp = self.__csp
        csp.update_domain("D1", {14})
        csp.update_domain("D2", {13.4})
        csp.update_domain("D3", {13, 13.1})
        csp.update_domain("D4", {12.5})
        csp.update_domain("D5", {11.5, 11.6})
        csp.update_domain("D6", {10.6})
        csp.update_domain("D7", {9})
        # act
        output = self.__sut.establish("D5", 11.6)
        # assess
        self.assertEqual(output[0], CONTRADICTION)
        self.assertEqual(output[1], {"D5", "D6", "D7"})
