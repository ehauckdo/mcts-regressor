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

### How are expressions represented in MCTS?

In this implementation of the Monte Carlo tree search, each node has no knowledge about what value it is storing or how much further down it can go in the tree. Everyone node has access to a single handler object, which is reponsible to return the appropriate value to be stored on these nodes. In other words, the tree node objects only know operations regarding the tree search, while the handler object only knows operations regarding expression manipulation.

The value to be stored at a single node is a component (or a list of components). A component can be either operators (e.g. +, -), or terminals (e.g. 0, 1, x). It is important to note that the representation of an expression within the tree search is different from the traditional expression tree. When a given expression in the tree search, given by a path from the node to a leaf node, is completed, this list of components are them converted to an expression tree. Refer to the image below to for a clear understanding. 

![alt text](https://i.imgur.com/euJaDI4.png)

From the image it is possible to notice that the expression in the tree search is represented in [reverse polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation). When setting an objective function through the command line, you must pass the function as a string using this notation. 

```
Expression in infix notation: x² + 2x + 4
Expression in reverse polish notation: add add pow x 2 mul 2 x add 2 2
```
The currently implemeted operators and terminals are:
```
add: numpy.add
sub: numpy.ubtract
mul: numpy.multiply
div: numpy.true_divide
cos: numpy.cos
sin: numpy.sin
pow: numpy.power
ln:  numpy.log
0: 0 (integer)
1: 1 (integer)
2: 2 (integer)
x, y, ... , w: variables
```
### MCTS details

Standard UCT (Upper Confidence bounds applied to Trees) is used as selection strategy for the search, and the reward is given by 1/(1+mse), where mse is the mean squared error of the results between the generated function and the objective function. There are no limitations regarding revisiting an explored branch or stopping after finding a 0 error expression.

### Folder structure
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
### Known problems

* This implementation use regular UCT, which according Cazanave is not very effective for the problem of symbolic regression.
* Although the error of the built expression is usually relatively small (MSE < 0.1) after finishing the search, most of the expressions found are linear, sometimes even without variables.
* If the domain allows an x so that the objective function return nan, inf or -inf, if the found expression doesn't return the same value for that x, the MSE will always be inf.  This problem will make it difficult to direct the search to the right place in the search space.
* The search can quickly converges to a local optimum (observed happening within 400 iterations).
* To pass an objective function, you need to break into components used by the program. This makes it impossible to use expressions without closed form, and can be very troublesome for complex expressions.

### Future ideas 

* Prevent re-searching into a subtree that was already fully explored (some executions converged to a local optimum very quickly, even though the 0 error solution was very close to be found in another branch of the tree)
* Iterative deepening: currently there is not criteria to decide the maximum depth of the tree (using the depth necessary to find the expression - cheating!). Iterative deepening could be a better solution for that
* Expand By Removing: consider the deletion of components as a possible expansion for the tree. This could (1) possibly improve the current implementation, (2) allows it to be executed like a video game: every x iterations, take the best child as root and restart the search from there.
