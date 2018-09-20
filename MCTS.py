from SearchNode import SearchNode
from SolutionHandler import SolutionHandler

class MCTS(object):

    def __init__(self, handler=SolutionHandler(), iterations=5000):
        self.iterations = iterations
        self.root = SearchNode(handler)
      
        for i in range(iterations): 
            self.root.iteration()
        result = self.root.bestBranch()
        print("Best: ")
        if len(handler.zeroErrorSolution) > 0:
            for sol in handler.zeroErrorSolution:
                print("Solution option: ")
                handler.printComponents(sol) 
        else:
            handler.printComponents(result) 

    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
        
