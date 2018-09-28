import logging
import StringIO
import time
from SearchNode import SearchNode
from SolutionHandler import SolutionHandler

logging.basicConfig(filename='log',level=logging.INFO, filemode='w')

class MCTS(object):

    def __init__(self, handler=SolutionHandler(), iterations=100000):
        self.iterations = iterations
        self.handler = handler
        self.root = SearchNode(handler)

    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
 
        if len(self.handler.zeroErrorSolution) > 0:
            for sol in self.handler.zeroErrorSolution:
                print("Solution option: \n"+"\n".join(self.handler.printComponents(sol)))
        else:
            result = self.root.bestBranch()
            print("Best brach: \n"+"\n".join(self.handler.printComponents(result)))

