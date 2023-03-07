def print_solution(solution, regs):
    all_vars = sorted(solution.keys(), key=lambda n: int(n[1:]))
    for s in range(0, 1000):
        if not "L"+str(s*7+1) in solution:
            break
        print("--------- "+regs[s]+" -----------")
        for i in range(1, 8):
            lvar = "L"+str(s*7+i)
            pvar = "P"+str(s*7+i)
            print("Node #"+str(i)+" => ",str(solution[lvar])+"mm of piece #"+solution[pvar][0], "  piece info:", solution[pvar])