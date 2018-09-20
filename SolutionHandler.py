
class SolutionHandler(object):
    def __init__(self):
        self.objective = None 
        self.expansion_limit = 0

    def addComponent(self, component):
        self.value.append(component)

    def getAvailableExpansions(self):
        return expansions

    def getNumberExpansionsPossible(self):
        return 0

    def expandSolution(self):
        return

    def getReward(self, valueHolder):
        return 0

    def getChildren(self, valueHolder):
        return 0

    def clear(self):
        self.value = {}
