#! /usr/bin/env python

from Utility.Utility import *
from Plot.Plot import *

# Small helper script to generate some charts

def main(args):
    prepareLogDirectory("figs/")

    expr = fetchExpressions("logs/f5/0/iterations")
    objective = fetchObjective("logs/f5/0/")

    plotAll(expr, objective)
    plotSearchStep()
    plotTwoByTwo(expr, objective)

    functions = ["logs/f5"]
    boxplot(functions)

if __name__ == '__main__':
    main(sys.argv[1:])
