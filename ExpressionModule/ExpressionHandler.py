import random
import logging
from sklearn.metrics import mean_squared_error
from SolutionHandler import SolutionHandler
from ExpressionModule.ExpressionNode import ExpressionNode
from ExpressionModule.ExpressionComponents import components

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
        logging.debug("Building expression tree...")
        rootNode = ExpressionNode(partialSolution[0])
        logging.debug("Created expression Root Node: "+str(partialSolution[0].value))
        for i in range(len(partialSolution)-1):
            logging.debug("Adding child: "+str(partialSolution[i+1].value))
            rootNode.addChild(partialSolution[i+1])

        objectiveRootNode = ExpressionNode(self.objective[0])
        for i in range(len(self.objective)-1):
            objectiveRootNode.addChild(self.objective[i+1])

        y_pred = []
        y_true = []

        logging.debug("Executing tree...")
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
            logging.info("Found 0 error solution!: "+self.printComponents(partialSolution))
            self.zeroErrorSolution.append(partialSolution)
        mse = -mse

        logging.debug("Expression Result for x= 5: "+str(rootNode.execute({"x":5})))
        logging.debug("Objective Result for x=5: "+str(objectiveRootNode.execute({"x":5})))

        return mse

    def getComponentsWithArityLessEqualThan(self, arity):
        comps = []
        for c in components:
            if c.arity <= arity: comps.append(c)
        return comps
    
    def printComponents(self, partialSolution=None):
        partialSolution = partialSolution if partialSolution != None else self.partialSolution
        string = ""
        for i in range(len(partialSolution)):
            string += "\n["+str(i)+"]: val="+str(partialSolution[i].value)+", ar="+str(partialSolution[i].arity)
            continue
            #return("["+str(i)+"]: val="+str(partialSolution[i].value)+", ar="+str(partialSolution[i].arity))
        if len(partialSolution) == 0:  
            return("*empty*")
        return string
    def clear(self):
        self.value = {}

