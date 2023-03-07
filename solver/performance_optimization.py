import cProfile
import pstats
import os.path as op
from sys import path as sp
current = op.dirname(op.realpath(__file__))
parent = op.dirname(current)
sp.append(parent)

from bb import main

if __name__ == "__main__":
    cProfile.run("main()", "speed_profile")
    p = pstats.Stats('speed_profile')
    p.strip_dirs()
    p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(20)