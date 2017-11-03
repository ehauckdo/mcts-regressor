#! /usr/bin/env python

from Utility.Utility import *
from Plot.Plot import *

# Small helper script to generate some charts

def main(args):
    prepareLogDirectory("figs/")

    expr = fetchExpressions("logs/iterations")
    objective = fetchObjective("logs/")

    plotAll(expr, objective)
    plotSearchStep()
    plotTwoByTwo(expr, objective)

if __name__ == '__main__':
    main(sys.argv[1:])
