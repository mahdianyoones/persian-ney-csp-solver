from spec import specs
from unary import get_pieces
from unary import UNARY
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

'''
Implements Branch and Bound to find the optimal solution.
'''

DS_PATH = "pieces.csv"

ALL_TYPES = {"Bb", "C", "A", "D", "G", "E", "F_tall", "F_short"}

values = {
    "Bb": 8,
    "C": 7,
    "A": 6,
    "D": 5,
    "G": 4,
    "E": 3,
    "F_tall": 2,
    "F_short": 1
}

costs = {
    "Bb": specs["Bb"]["len"],
    "C": specs["C"]["len"],
    "A": specs["A"]["len"],
    "D": specs["D"]["len"],
    "G": specs["G"]["len"],
    "E": specs["E"]["len"],
    "F_tall": specs["F_tall"]["len"],
    "F_short": specs["F_short"]["len"]
}

def cal_capacity():
    '''Sums up the length of all pieces found in the dataset.'''
    pieces = get_pieces(DS_PATH)
    capacity = 0
    for piece in pieces:
        capacity += piece[1] # len
    return capacity

CAPACITY = cal_capacity()
KOOKS_RSORTED = ["F_short", "E", "D", "C", "Bb", "A", "G", "F_tall"]
weight_variation = 3
weight_value = 2
weight_count = 1

def gen_items():
    '''Generates all possible instruments and sorts them greedily!'''
    all = {}
    for kook, spec in specs.items():
        count = int(CAPACITY // spec['len'])
        all[kook] = [kook for i in range(count, 0, -1)]
    items = []
    all_appended = False
    kooks = sorted(specs.keys(), key=lambda kook: values[kook], reverse=True)
    while not all_appended:
        all_appended = True
        for kook in kooks:
            if len(all[kook]) > 0:
                items.append(all[kook].pop())
                if len(all[kook]):
                    all_appended = False
    return items

def satisfiable(node_combination):
    costs_sum = 0
    for kook in node_combination:
        costs_sum += costs[kook]
    if costs_sum > CAPACITY:
        return False
    csp = CSP(len(node_combination))
    select = SELECT(csp)
    mac = MAC(csp, specs[kook])
    UNARY.init_domains(csp, DS_PATH)
    res = UNARY.unarify(csp, specs[kook])
    if res == CONTRADICTION:
        return False # No solution could exist. Unary constaints violated!
    solver = SOLVER(csp, select, mac)
    indicator, solution = solver.find_independent(specs[kook], DS_PATH)
    if indicator == SOLUTION:
        if is_valid(solution, kook):
            return True
        else:
            raise Exception("Found an invalid solution ", solution)
    return False

def normalize_values_sum(values_sum):
    best_kook = list(values.keys())[0]
    best_value = values[best_kook]
    best_len = specs[best_kook]["len"]
    max_best = CAPACITY // best_len
    return values_sum / (best_value * int(max_best))

def normalize_count(count):
    best_kook = list(values.keys())[0]
    best_len = specs[best_kook]["len"]
    max_best = CAPACITY // best_len
    return count / max_best

def values_sum(candidate):
    values_sum = 0
    for kook in candidate:
        values_sum += values[kook]
    return values_sum

def calc_utility(candidate):
    values_sum_normalized = normalize_values_sum(values_sum(candidate))
    count_normalized = normalize_count(len(candidate))
    variation_normalized = len(set(candidate)) / len(values.keys())
    return variation_normalized * weight_variation + \
        values_sum_normalized * weight_value + \
            count_normalized * weight_count

def variation_estimate(node_combination, left_capacity):
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
    occupied_types = set(node_combination)
    variation = len(occupied_types)
    for possible_kook in KOOKS_RSORTED:
        if possible_kook in occupied_types:
            continue
        if costs[possible_kook] > left_capacity:
            break
        variation += 1
        left_capacity -= costs[possible_kook]
    return variation

def count_estimate(left_capacity):
    '''Determines the maximum number of possible instruments
    
    that could be constructed with the left pieces.'''
    return left_capacity // costs[KOOKS_RSORTED[0]]

def value_estimate(left_capacity):
    '''Determines the maximum value of possible instruments
    
    that could be constructed with the left pieces.'''
    values_sum = 0
    for kook, value in values.items():
        while left_capacity > costs[kook]:
            values_sum += value
            left_capacity -= costs[kook]        
    return values_sum

def normalize_variation(variation):
    return variation / 8

def utility_bound(node_combination, node_utility, node_cost):
    left_capacity = CAPACITY - node_cost
    max_variation = variation_estimate(node_combination, left_capacity)
    max_value = value_estimate(left_capacity)
    max_count = count_estimate(left_capacity)
    max_variation_normalized = normalize_variation(max_variation)
    max_value_normalized = normalize_values_sum(max_value)
    max_count_normalized = normalize_count(max_count)
    bound = weight_variation * max_variation_normalized 
    bound += weight_value * max_value_normalized
    bound += weight_count * max_count_normalized
    bound += node_utility
    return bound

items = gen_items()

solutions = [(0, 0, [], 0)]
best_utility = 0
best_combination = []
optimal_solution = []

nodes_counter = 0

while len(solutions) > 0:
    node_utility, node_cost, node_combination, child_index = solutions.pop()
    # Leaf? Backtrack.
    if child_index == len(items):
        if best_utility > node_utility:
            optimal_solution = deepcopy(best_combination)
        else:
            optimal_solution = deepcopy(node_combination)
        continue
    # Branching based on exclusion of the child
    without_combination = deepcopy(node_combination)
    node_without = (node_utility, node_cost, without_combination, child_index + 1)
    solutions.append(node_without)
    nodes_counter += 1
    # Branching based on inclusion of the child
    with_combination = deepcopy(node_combination)
    with_combination.append(items[child_index])
    if satisfiable(with_combination):
        with_utility = calc_utility(with_combination)
        with_cost = node_cost + costs[items[child_index]]
        if with_utility > best_utility:
            best_utility = with_utility
            best_combination = deepcopy(with_combination) # copy
        if utility_bound(with_combination, with_utility, with_cost) > best_utility:
            node_with = (with_utility, with_cost, with_combination, child_index + 1)
            solutions.append(node_with)
            nodes_counter += 1
    if nodes_counter % 20000 == 0:
        print(nodes_counter)

print(optimal_solution)