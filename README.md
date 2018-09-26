# Python MCTS implementation

This repository provides an implementation of the Monte Carlo Tree Search algorithm using Python 2.7. 
It aims to be as a generic implementation as possible, allowing for multiple applications.
Each new application requires a new module which should inherit from SolutionHandler.

# Symbolic Regression Module

The ExpressionModule folder contains the module for symbolic regression via MCTS. 
It uses a list of components (which can be operators/nodes or operands/terminals) that make up the tree search.
After a certain expression (list of components) is decided during the search, an expression tree is built from these components and the mean square error is used as reward for the search.
