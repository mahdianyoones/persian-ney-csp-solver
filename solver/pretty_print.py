def print_solution(solution):
    print("--------------------")
    all_vars = sorted(solution.keys(), key=lambda n: int(n[1:]))
    pvars_sorted = [pvar for pvar in all_vars if pvar[0] == "P"]
    lvars_sorted = [lvar for lvar in all_vars if lvar[0] == "L"]
    for pvar in pvars_sorted:
        print(pvar, ": ", solution[pvar])
    for lvar in lvars_sorted:
        print(lvar, ": ", solution[lvar])