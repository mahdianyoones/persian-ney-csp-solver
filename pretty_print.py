def print_solution(solution, regs):
    msg = ""
    for s in range(0, 1000):
        if not "L"+str(s*7+1) in solution:
            break
        msg += "--------- "+regs[s]+" -----------"  + "\n"
        for i in range(1, 8):
            lvar = "L"+str(s*7+i)
            pvar = "P"+str(s*7+i)
            msg += "Node #"+str(i)+" => "
            msg += str(solution[lvar])+"mm of piece #"+solution[pvar][0]
            msg += "  piece info:" + str(solution[pvar]) + "\n"
    return msg
        

def print_stats(stats):
    msg = "----------------------------------" + "\n\n"
    msg += "Generated nodes: " + str(stats["nodes"]) + "\n"
    msg += "Backjumps: " + str(stats["backjumps"]) + "\n"
    msg += "Backtracks: " + str(stats["backtracks"]) + "\n"
    return msg