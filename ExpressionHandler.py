import random
from sklearn.metrics import mean_squared_error
from SolutionHandler import SolutionHandler
from ExpressionNode import ExpressionNode
from ExpressionComponents import components 

class ExpressionHandler(SolutionHandler):

    def __init__(self):
        self.objective = None
        self.partialSolution = []
        self.maxSolutionSize = 0
        self.zeroErrorSolution = []

    def getNumberTerminalsAllowed(self, partialSolution=None):
        partialSolution = partialSolution if partialSolution != None else self.partialSolution
        terminalsAllowed = 1
        for component in partialSolution:
            terminalsAllowed -= 1
            terminalsAllowed += component.arity
        return terminalsAllowed

    def expandSolution(self, partialSolution=None):
        partialSolution = partialSolution if partialSolution != None else self.partialSolution
        terminals_possible = self.getNumberTerminalsAllowed(partialSolution)
        maxSolutionSize = self.maxSolutionSize
        currentSize = len(partialSolution)

        if terminals_possible == 0 or currentSize >= maxSolutionSize:
            return False

        arity_allowed = maxSolutionSize - (terminals_possible + currentSize)

        terminals_possible = self.getComponentsWithArityLessEqualThan(arity_allowed)
        partialSolution.append(random.choice(terminals_possible))
        return True

    def getPossibleChildren(self, partialSolution):
        terminalsAllowed = self.getNumberTerminalsAllowed(partialSolution)
        sizeLimit = self.maxSolutionSize
        currentSize = len(partialSolution)

        if terminalsAllowed == 0 or currentSize >= sizeLimit:
            return []

        arityAllowed = sizeLimit - (terminalsAllowed + currentSize)
        possibleChildren = self.getComponentsWithArityLessEqualThan(arityAllowed)
        return possibleChildren

    def getReward(self, partialSolution):
        print("-- Begin REWARD calculation --")
        rootNode = ExpressionNode(partialSolution[0])
        print("Created root Node: "+str(partialSolution[0].value))
        for i in range(len(partialSolution)-1):
            print("Adding child: "+str(partialSolution[i+1].value))
            rootNode.addChild(partialSolution[i+1])

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
        #print("y_pred: ")
        #print(y_pred)
        #print("y_true: ")
        #print(y_true)
        mse = mean_squared_error(y_true, y_pred)
        if mse == 0:
            print("Found 0 error solution!: ")
            self.printComponents(partialSolution)
            self.zeroErrorSolution.append(partialSolution)
        mse = -mse

        print("Objective result: "+str(objectiveRootNode.execute({"x":5})))
        result = rootNode.execute({"x":5})
        print("Result: "+str(result))
        print("-- Finished REWARD calculation --")

        return mse
        #return result

    def getComponentsWithArityLessEqualThan(self, arity):
        comps = []
        for c in components:
            if c.arity <= arity: comps.append(c)
        return comps
    
    def printComponents(self, partialSolution=None):
        partialSolution = partialSolution if partialSolution != None else self.partialSolution
        for i in range(len(partialSolution)):
            print("["+str(i)+"]: ", partialSolution[i].value, partialSolution[i].arity)
        else:
            print("*empty*")
    
    def clear(self):
        self.value = {}

