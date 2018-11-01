# Symbolic Regression via Monte Carlo Tree Search (MCTS)

This repository provides a symbolic regressor via the MCTS algorithm, implemented in Python 2.7. 

### Usage

```Usage: python regression [options]

Options:
  -h, --help         show this help message and exit
  -l FOLDER          Select the folder to save results
  -v NUMVARS         The number of variables to use for regression
  -i ITERATIONS      The number of MCTS iterations
  -o OBJECTIVE       Objective function in polish notation
  -d DEPTH           The maximum tree depth
  -s SEED            Seed for this execution
  --lower=LOWER      Lower value for samples
  --upper=UPPER      Upper value for samples
  --points=POINTS    Number of equally spaced points between upper and lower
                     bounds
  --samples=SAMPLES  Number of samples to be selected from domain
```

### Implementation details

```
.
└── mcts-regressor
    ├── MCTS                          # General MCTS implementation, SolutionHandler.py can be extended
    │   ├── __init__.py               # to apply this algorithm in other applications
    │   ├── MCTS.py
    │   ├── SearchNode.py
    │   └── SolutionHandler.py
    ├── ExpressionModule              # Implementation of SolutionHandler to perform symbolic regression
    │   ├── ExpressionComponents.py
    │   ├── ExpressionHandler.py
    │   ├── ExpressionNode.py
    │   └── __init__.py
    ├── Plot                          # Provide functions to facilitate vizualition of results
    │   ├── __init__.py
    │   └── Plot.py
    ├── Utility                       # Utility functions
    │   ├── __init__.py
    │   └── Utility.py
    ├── plot
    ├── README.md
    └── regression
```

### How are expressions represented in MCTS?

In this implementation of the Monte Carlo tree search, each node has no knowledge about what value it is storing or how much further down it can go in the tree. The ExpressionHandler (inherited from the general object SolutionHandler) is a single object that every node has access, and which is reponsible to return the appropriate value for these nodes. In other words, the SearchNode objects only know operations regarding the tree search, while the ExpressionHandler object only knows operations regarding expression manipulation. 

The ExpressionHandler assign a ExpressionComponent to each tree node. ExpressionNodes can be either operators (e.g. +, -), in which case they have arity greater than 0, or terminals (e.g. 0, 1, x). Expressions are represented using reverse polish notation.

```
Expression in infix notation: x² + 2x + 4
Expression in reverse polish notation: add add pow x 2 mul 2 x add 2 2
```
The currently implemeted operators and terminals are:

```
"add": numpy.add
"sub": numpy.ubtract
"mul": numpy.multiply
"div": numpy.true_divide
"cos": numpy.cos
"sin": numpy.sin
"pow": numpy.power
"ln":  numpy.log
0: 0 (integer)
1: 1 (integer)
2: 2 (integer)
"x", "y", ... , "w": variables
```
