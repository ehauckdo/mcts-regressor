from SearchNode import SearchNode
from PartialSolution import *
from copy import deepcopy

class MCTS(object):

    def __init__(self, objective="", iterations=1500):
        self.objective = objective
        empty_part_sol = deepcopy(objective)
        self.iterations = iterations
        self.root = SearchNode(None, empty_part_sol)
        self.root.objective = objective
        
    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
        
