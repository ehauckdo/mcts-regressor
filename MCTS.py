from SearchNode import SearchNode
from PartialSolution import *
from Utility import *

class MCTS(object):

    def __init__(self, objective="", iterations=1500):
        self.objective = objective
        self.iterations = iterations
        empty_solution = instantiateNewObject(objective)
        self.root = SearchNode(None, empty_solution)
        self.root.objective = objective
        
    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
        
