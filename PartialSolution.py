from operator import __add__,__sub__,__mul__

class PartialSolution(object):
    def __init__(self, value={}):
        self.value = value

    def addComponent(self, component):
        self.value.append(component)

    def getAvailableExpansions(self):
        return expansions

    def getReward(self):
        return 0

    def clear(self):
        self.value = {}

class PartialExpression(PartialSolution):

    def __init__(self, value={}):
        self.value = value

    def addComponent(self, component):
        self.value.append(component) # we can build a tree here
                                    # instead of using a list

    def getAvailableExpansions(self):
        return expansions

    def getReward(self):
        return 0
    
    def clear(self):
        self.value = {}

class ExpressionComponent(object):

    def __init__(self, value, arity):
        self.value = value
        self.arity = arity

expansions = [ExpressionComponent(1, 0),
                ExpressionComponent(2, 0),
                ExpressionComponent("x", 0),
                ExpressionComponent(__add__, 2),
                ExpressionComponent(__sub__,2),
                ExpressionComponent(__mul__, 2)]

