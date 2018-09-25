import random
import logging
import sys
from sklearn.metrics import mean_squared_error
from SolutionHandler import SolutionHandler
from ExpressionModule.ExpressionNode import ExpressionNode
from ExpressionModule.ExpressionComponents import components

class ExpressionHandler(SolutionHandler):

    def __init__(self, objective=None):
        self.objective = objective
        self.partialSolution = []
        self.maxSolutionSize = 0
        self.executeObjectiveTree() 
        self.zeroErrorSolution = []
        self.zeroErrorSolutionHashs = []
        self.bestSolutionSoFar = (None, -sys.maxint)
        self.iterationCount = 0

    def executeObjectiveTree(self):
        objectiveRootNode = ExpressionNode(self.objective[0])
        for i in range(len(self.objective)-1):
            objectiveRootNode.addChild(self.objective[i+1])
        test_value = -10
        self.y_true = []
        while test_value <= 10:
            objectiveResult = objectiveRootNode.execute({'x':test_value})
            self.y_true.append(objectiveResult)
            test_value += 0.5

    def getPossibleChildren(self, partialSolution):
        terminalsAllowed = self.getNumberTerminalsAllowed(partialSolution)
        sizeLimit = self.maxSolutionSize
        currentSize = len(partialSolution)

        if terminalsAllowed == 0 or currentSize >= sizeLimit:
            return []

        arityAllowed = sizeLimit - (terminalsAllowed + currentSize)
        possibleChildren = self.getComponentsWithArityLessEqualThan(arityAllowed)
        return possibleChildren
    
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


    def getReward(self, partialSolution):
        #logging.debug("Building expression tree...")
        #rootNode = ExpressionNode(partialSolution[0])
        #logging.debug("Created expression Root Node: "+str(partialSolution[0].value))
        #for i in range(len(partialSolution)-1):
        #    logging.debug("Adding child: "+str(partialSolution[i+1].value))
        #    rootNode.addChild(partialSolution[i+1])

        #objectiveRootNode = ExpressionNode(self.objective[0])
        #for i in range(len(self.objective)-1):
        #    objectiveRootNode.addChild(self.objective[i+1])

        #y_pred = []

        #logging.debug("Executing tree...")
        #test_value = -10
        #while test_value <= 10:
        #    expressionResult = rootNode.execute({"x":test_value})
        #    y_pred.append(expressionResult)
        #    test_value += 0.5

        y_pred = self.buildAndExecuteTree(partialSolution)
        #logging.debug("y_pred: ")
        #logging.debug(y_pred)
        #logging.debug("y_true: ")
        #logging.debug(y_true)
        mse = mean_squared_error(self.y_true, y_pred)
        if mse == 0:
            solutionHash = hash(tuple(partialSolution))
            logging.info("0 error solution found! Hash: "+str(solutionHash))
            if solutionHash not in self.zeroErrorSolutionHashs:
                self.zeroErrorSolution.append(partialSolution)
                self.zeroErrorSolutionHashs.append(solutionHash)
        else:
            mse = -mse

        #logging.info("Expression Result for x=5: "+str(rootNode.execute({"x":5})))
        #logging.info("Objective Result for x=5: "+str(objectiveRootNode.execute({"x":5})))

        if mse > self.bestSolutionSoFar[1]:
            self.bestSolutionSoFar = (partialSolution, mse)

        self.logBestResult()
        return mse

    def buildAndExecuteTree(self, partialSolution):
        rootNode = ExpressionNode(partialSolution[0])
        for i in range(len(partialSolution)-1):
            logging.debug("Adding child: "+str(partialSolution[i+1].value))
            rootNode.addChild(partialSolution[i+1])
        
        objectiveRootNode = ExpressionNode(self.objective[0])
        for i in range(len(self.objective)-1):
            objectiveRootNode.addChild(self.objective[i+1])
        
        y_pred = []

        logging.debug("Executing tree...")
        test_value = -10
        while test_value <= 10:
            expressionResult = rootNode.execute({"x":test_value})
            y_pred.append(expressionResult)
            test_value += 0.5
        return y_pred

    def getNumberTerminalsAllowed(self, partialSolution=None):
        partialSolution = partialSolution if partialSolution != None else self.partialSolution
        terminalsAllowed = 1
        for component in partialSolution:
            terminalsAllowed -= 1
            terminalsAllowed += component.arity
        return terminalsAllowed

    def getComponentsWithArityLessEqualThan(self, arity):
        comps = []
        for c in components:
            if c.arity <= arity: comps.append(c)
        return comps
    
    def printComponents(self, partialSolution=None):
        partialSolution = partialSolution if partialSolution != None else self.partialSolution
        if len(partialSolution) == 0:  
            return(["*empty*"])
        
        string = []
        for i in range(len(partialSolution)):
            string.append("val="+str(partialSolution[i].value)+", ar="+str(partialSolution[i].arity))
        return string

    def logBestResult(self):
        self.iterationCount +=1
        if self.iterationCount % 100 == 0:
            logging.info("Best solution so far (reward:"+str(self.bestSolutionSoFar[1])+"): ")
            y_pred = self.buildAndExecuteTree(self.bestSolutionSoFar[0])
            with open('result/result'+str(self.iterationCount/100)+'.csv', 'w') as f:
                f.write("-10,10,0.5\n")
                f.write("\n".join([str(y) for y in y_pred]))

