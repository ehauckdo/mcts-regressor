
class SolutionHandler(object):
    def __init__(self):
        self.objective = None
        self.partialSolution = [] 
        self.maxSolutionSize = 0

    def addComponent(self, component):
        self.value.append(component)

    def expandSolution(self):
        return

    def getReward(self, valueHolder):
        return 0

    def getPossibleChildren(self, valueHolder):
        return 0

    def printComponents(self, partialSolution):
        for components in partialSolution:
            print(components)

    def clear(self):
        self.value = {}
