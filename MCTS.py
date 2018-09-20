from SearchNode import SearchNode
from ExpressionHandler import *
from Utility import *
import importlib

class MCTS(object):

    def __init__(self, handler=SolutionHandler(), iterations=1500):
        self.iterations = iterations
        self.root = SearchNode(handler)
      
        for i in range(10000): 
            self.root.iteration()
        result = self.root.bestChild()
        print("Best: ")
        if len(handler.solution) > 0:
            for sol in handler.solution:
                print("Solution option: ")
                handler.printValue(sol) 
        else:
            handler.printValue(result) 

    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
        
