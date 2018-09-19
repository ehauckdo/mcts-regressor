from SearchNode import SearchNode
from SolutionHandler import *
from Utility import *
import importlib

class MCTS(object):

    def __init__(self, handler=SolutionHandler(), iterations=1500):
        self.iterations = iterations
        self.root = SearchNode(handler)
      
        for i in range(100): 
            self.root.iteration()
        result = self.root.bestChild()
        print("Best: ")
        handler.printValue(result) 

    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
        
