import logging
from SearchNode import SearchNode
from SolutionHandler import SolutionHandler

logging.basicConfig(filename='log',level=logging.INFO, filemode='w')

class MCTS(object):

    def __init__(self, handler=SolutionHandler(), iterations=5000):
        self.iterations = iterations
        self.root = SearchNode(handler)
        for i in range(iterations): 
            self.root.iteration()

        if len(handler.zeroErrorSolution) > 0:
            for sol in handler.zeroErrorSolution:
                print("Solution option: ")
                
                print(handler.printComponents(sol)) 
        else:
            result = self.root.bestBranch()
            print("Best: ")
            print(handler.printComponents(result))

    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
        
