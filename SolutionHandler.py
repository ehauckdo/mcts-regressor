
class SolutionHandler(object):
    def __init__(self):
        self.objective = None
        self.partialSolution = [] 
        self.maxSolutionSize = 0
    
    def getPossibleChildren(self, partialSolution):
        return 0

    def expandSolution(self, partialSolution=None):
        return

    def getReward(self, partialSolution):
        return 0

    def printComponents(self, partialSolution):
        for components in partialSolution:
            print(components)

