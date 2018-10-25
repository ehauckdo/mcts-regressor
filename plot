#! /usr/bin/env python

from Utility.Utility import *
from Plot.Plot import *

def main(args):
    prepareLogDirectory("figs/")

    expr = fetchExpressions("logs/iterations")
    objective = fetchObjective("logs/")

    plotAll(expr, objective)
    plotSearchStep()
    plotTwoByTwo(expr, objective)

    #expr["Objective"] = objective

if __name__ == '__main__':
    main(sys.argv[1:])
