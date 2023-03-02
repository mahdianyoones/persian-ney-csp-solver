from spec import specs as reg_specs
from unary import get_pieces
from copy import deepcopy
import os
from sys import path as sp
from solver import SOLVER
from csp import CSP
from mac import MAC
from pickup import SELECT
from constants import *
from verify import is_valid

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sp.append(parent)

class SAT:
    
    def __init__(self, capacity, costs, specs, ds_path):
        self.__select = SELECT()
        self.__mac = MAC()
        self.__solver = SOLVER(self.__select, self.__mac)
        self.__capacity = capacity
        self.__costs = costs
        self.__specs = specs
        self.__ds_path = ds_path

    def __too_long(self, node_items):
        if sum([self.__costs[reg] for reg in node_items]) > self.__capacity:
            return True
        return False

    def __psp(self, node_items, solution):
        '''Prints solution prettily!'''
        j = 0
        for kook in node_items:
            print(kook, " : ")
            msg = "Ls ("
            for i in range(1, 8):
                msg += str(solution["L"+str(j*7+i)])
                msg += ","
            msg += ")"
            print(msg)
            for i in range(1, 8):
                print(str(solution["P"+str(j*7+i)]))
            print("----")
            j += 1
        print("================")

    def satisfiable(self, node_items):
        '''Creates a new CSP problem for them given candidate solution
        
        and checks if it is satisfiable.'''
        if self.__too_long(node_items):
            return False
        csp = CSP(S=len(node_items))
        specs_sorted = [self.__specs[reg] for reg in node_items]
        indicator, solution = self.__solver.find(csp, specs_sorted, self.__ds_path)
        if indicator == SOLUTION:
            if not is_valid(solution, node_items):
                self.__psp(node_items, solution)
                raise Exception("Invalid solution")
            return True
            # do something with solution
            # e.g. check the validity of the solution, store it etc
        return False

class UTILITY:

    def __init__(self, capacity, costs, specs, regs, values):
        self.__values = values
        self.__capacity = capacity
        self.__costs = costs
        self.__specs = specs
        self.__regs_rsorted = sorted(regs, \
            key=lambda reg: specs[reg]["len"], reverse=True)
        self.__w_variation = 3
        self.__w_value = 2
        self.__w_count = 1

    def __normalize_value(self, value):
        best_reg = list(self.__values.keys())[0]
        best_value = self.__values[best_reg]
        best_len = self.__specs[best_reg]["len"]
        max_best = self.__capacity // best_len
        return value / (best_value * int(max_best))

    def __normalize_count(self, count):
        best_reg = list(self.__values.keys())[0]
        best_len = self.__specs[best_reg]["len"]
        max_best = self.__capacity // best_len
        return count / max_best

    def items_utility(self, items):
        values_sum = sum([self.__values[reg] for reg in items])
        values_sum_normalized = self.__normalize_value(values_sum)
        count_normalized = self.__normalize_count(len(items))
        variation = len(set(items))
        variation_normalized = variation / len(self.__values.keys())
        return variation_normalized * self.__w_variation + \
            values_sum_normalized * self.__w_value + \
                count_normalized * self.__w_count

    def __variation_estimate(self, node_items, left_capacity):
        '''Estimates the maximum possible variation.
        
        i.e. determine the maximmum number of instrument types that
        can be possibly built given the left capacity minus 
        the number of types in the current_items.
        
        For instance, if current_items = {F_tall, F_tall, F_tall}, and
        left_capacity = 100:

        100 - len of F_short = 61
        61 - lef of E = 20

        Therefore, 1 + 2 = 3 varied instruments is possible, where 1 is the
        types in the current_items and 2 is the maximum possible types.

        Variation is a value between 1 and 8.
        8 is the total number of instrument types.'''
        occupied_types = set(node_items)
        variation = len(occupied_types)
        for possible_reg in self.__regs_rsorted:
            if possible_reg in occupied_types:
                continue
            if self.__costs[possible_reg] > left_capacity:
                break
            variation += 1
            left_capacity -= self.__costs[possible_reg]
        return variation

    def __count_estimate(self, left_capacity):
        '''Determines the maximum number of possible instruments
        
        that could be constructed with the left pieces.'''
        return left_capacity // self.__costs[self.__regs_rsorted[0]]

    def __value_estimate(self, left_capacity):
        '''Determines the maximum value of possible instruments
        
        that could be constructed with the left pieces.'''
        values_sum = 0
        for kook, value in self.__values.items():
            while left_capacity > self.__costs[kook]:
                values_sum += value
                left_capacity -= self.__costs[kook]      
        return values_sum

    def bound(self, node_items, node_utility, node_cost):
        left_capacity = self.__capacity - node_cost
        max_variation = self.__variation_estimate(node_items, left_capacity)
        max_value = self.__value_estimate(left_capacity)
        max_count = self.__count_estimate(left_capacity)
        max_variation_normalized = max_variation / len(self.__values.keys())
        max_value_normalized = self.__normalize_value(max_value)
        max_count_normalized = self.__normalize_count(max_count)
        bound = self.__w_variation * max_variation_normalized 
        bound += self.__w_value * max_value_normalized
        bound += self.__w_count * max_count_normalized
        bound += node_utility
        return bound
        
class BB:
    '''Implements Branch and Bound to find the optimal solution.'''

    def __init__(self, ds_path, regs, specs):
        capacity = sum([piece[1] for piece in get_pieces(ds_path)])
        values =  {
            "Bb": 8, "C": 7, "A": 6, "D": 5, "G": 4, 
            "E": 3, "F_tall": 2, "F_short": 1
        }
        costs = {reg: specs[reg]["len"] for reg in regs}
        self.__capacity = capacity
        self.__specs = specs
        self.__regs = regs
        self.__values = values
        self.__costs = costs
        self.__sat = SAT(capacity, costs, specs, ds_path)
        self.__ut = UTILITY(capacity, costs, specs, regs, values)

    def __gen_items(self, specs, capacity, values):
        '''Generates all possible instruments and sorts them greedily!
        
        Each item is a hypothetical instrument that may or may not be built.
        To produce combinations like {Bb, Bb, C, C, G}, check their utility,
        and satisfiability, we resort to combinaorial counting principles!

        What is the maximum number of instruments constructable via the given
        pieces? 

        We don't know.

        If we could answer this questions precisely and accurately, then the 
        problem would be much easier to solver. 
        
        That is, the nature of pieces and constraints dictates this unknown
        number.

        However, since we are not trying to answer this question, we relax
        all the constraints except the length, which is predictable
        and precise.

        relaxed maximum number of viable instruments = 
            Sum(length of all pieces) / length of the instrument type

        With the data set at hand, there are 1200 / 39 = 30 maximum instruments,
        where 39 is the length of F_short and 1200 is the length sum of all pieces.

        That is, if we relaxed all constraints, we could at most build 30
        instruments of type F_short.

        For Bb, there would be at most 1200 / 59 = 20 instruments.
        For A, there would be at most 1200 / 59 = 19 instruments.
        and so on

        Now, the right question is 'how many of which instrument type would
        yield the highest utility?

        Again, since we don't know if, say, 20 instruments of type Bb is
        possible or not, we need to consider this combination as well as many
        similar combinations.

        Therefore, we generate 20 Bb items, 10 A items, and so on. The resulting
        items would be:

        Bb  consider / not cinsider
        Bb  consider / not cinsider
        Bb  consider / not cinsider

        ... 16 similar items in between

        Bb  consider / not cinsider

        A  consider / not cinsider
        A  consider / not cinsider
        A  consider / not cinsider

        ... 16 similar items in between

        A  consider / not cinsider

        and so on for other kooks.

        This way BB algorithm can sequentially iterate over items and do its
        job while not exluding any possibility.
        
        This item generation approach gauarantees that THE BEST VIABLE COMBINATION
        is not missed.'''
        all = {}        
        for reg, spec in specs.items():
            count = int(capacity // spec['len'])
            all[reg] = [reg for i in range(count, 0, -1)]
        items = []
        all_appended = False
        # regs reverse sorted based on values
        rvalregs = sorted(specs.keys(), 
            key=lambda reg: values[reg], reverse=True) 
        while not all_appended:
            all_appended = True
            for reg in rvalregs:
                if len(all[reg]) > 0:
                    items.append(all[reg].pop())
                    if len(all[reg]):
                        all_appended = False
        return items

    def find(self):
        all_items = self.__gen_items(self.__specs, self.__capacity, self.__values)
        solutions = [(0, 0, [], 0)]
        best_utility = 0
        best_solution = []
        optimal_solution = []
        nodes_counter = 0
        while len(solutions) > 0:
            # current node
            utility, cost, items, child_index = solutions.pop()
            # Leaf? Backtrack.
            if child_index == len(all_items):
                if best_utility > utility:
                    optimal_solution = deepcopy(best_solution)
                else:
                    optimal_solution = deepcopy(items)
                continue
            # Branching based on exclusion of the child
            without = (utility, cost, deepcopy(items), child_index + 1)
            solutions.append(without)
            nodes_counter += 1
            # Branching based on inclusion of the child
            with_items = deepcopy(items)
            with_items.append(all_items[child_index])
            if self.__sat.satisfiable(with_items):
                with_utility = self.__ut.items_utility(with_items)
                with_cost = cost + self.__costs[all_items[child_index]]
                if with_utility > best_utility:
                    best_utility = with_utility
                    best_solution = deepcopy(with_items) # copy
                if self.__ut.bound(with_items, with_utility, with_cost) > best_utility:
                    _with = (with_utility, with_cost, with_items, child_index + 1)
                    solutions.append(_with)
                    nodes_counter += 1
        return optimal_solution
    
def main():
    regs = {"F_tall", "G", "A", "Bb", "C", "D", "E", "F_short"}
    bb = BB("pieces.csv", regs, reg_specs)
    optimal_solution = bb.find()
    print(optimal_solution)

if __name__ == "__main__":
    main()