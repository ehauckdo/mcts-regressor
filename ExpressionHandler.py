import random
from sklearn.metrics import mean_squared_error
from SolutionHandler import SolutionHandler
from ExpressionNode import ExpressionNode
from ExpressionComponents import components 

class ExpressionHandler(SolutionHandler):

    def __init__(self):
        self.objective = None
        self.valueHolder = []
        self.expansion_limit = 0
        self.solution = []

    def addComponent(self, component):
        self.value.append(component)

    def getNumberExpansionsPossible(self, value=None):
        value = value if value != None else self.valueHolder
        movesLeft = 1
        for component in value:
            movesLeft -= 1
            movesLeft += component.arity
        return movesLeft

    def expandSolution(self, value=None):
        value = value if value != None else self.valueHolder
        # getNumberExpansionsPossible can have a better naming...
        expansions_possible = self.getNumberExpansionsPossible(value)
        expansion_limit = self.expansion_limit
        current_depth = len(value)

        if expansions_possible == 0 or current_depth >= expansion_limit:
            return False

        arity_allowed = expansion_limit - (expansions_possible + current_depth)

        expansions_possible = self.getComponentsWithArityLessEqualThan(arity_allowed)
        value.append(random.choice(expansions_possible))
        return True

    def getComponentsWithArityLessEqualThan(self, arity):
        comps = []
        for c in components:
            if c.arity <= arity: comps.append(c)
        return comps
    
    def getChildren(self, valueHolder):
        expansions_possible = self.getNumberExpansionsPossible(valueHolder)
        expansion_limit = self.expansion_limit
        current_depth = len(valueHolder)

        if expansions_possible == 0 or current_depth >= expansion_limit:
            return []

        arity_allowed = expansion_limit - (expansions_possible + current_depth)
        expansions_possible = self.getComponentsWithArityLessEqualThan(arity_allowed)
        return expansions_possible

    def getReward(self, valueHolder):
        rootNode = ExpressionNode(valueHolder[0])
        print("Created root Node: "+str(valueHolder[0].value))
        for i in range(len(valueHolder)-1):
            print("Adding child: "+str(valueHolder[i+1].value))
            rootNode.addChild(valueHolder[i+1])

        objectiveRootNode = ExpressionNode(self.objective[0])
        for i in range(len(self.objective)-1):
            objectiveRootNode.addChild(self.objective[i+1])

        y_pred = []
        y_true = []

        print("calculating reward")
        test_value = -10
        while test_value <= 10:
            #value = rootNode.execute({"x":test_value})
            #obj_value = objectiveRootNode.execute({'x':test_value})
            #print("Test_value: "+str(test_value))
            #print(str(value)+" --- "+str(obj_value))
            y_pred.append(rootNode.execute({"x":test_value}))
            y_true.append(objectiveRootNode.execute({'x':test_value}))
            test_value += 0.5
        print("y_pred: ")
        print(y_pred)
        print("y_true: ")
        print(y_true)
        mse = mean_squared_error(y_true, y_pred)
        if mse == 0:
            print("Found 0 error solution!: ")
            self.printValue(valueHolder)
            self.solution.append(valueHolder)
        mse = -mse

        print("Objective result: "+str(objectiveRootNode.execute({"x":5})))
        result = rootNode.execute({"x":5})
        print("Result: "+str(result))

        return mse
        #return result

    def printValue(self, value=None):
        value = value if value != None else self.valueHolder
        for i in range(len(value)):
            print("["+str(i)+"]: ", value[i].value, value[i].arity)

    def clear(self):
        self.value = {}

