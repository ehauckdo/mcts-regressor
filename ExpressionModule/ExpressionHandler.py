import random
import logging
import sys
import os, shutil
import numpy as np
from collections import namedtuple
from sklearn.metrics import mean_squared_error
from SolutionHandler import SolutionHandler
from ExpressionModule.ExpressionNode import ExpressionNode
from ExpressionModule.ExpressionComponents import components

class ExpressionHandler(SolutionHandler):

    def __init__(self, objective=None, lower=-10, upper=10, step=0.5):
        self.objective = objective
        self.partialSolution = []
        self.maxSolutionSize = 0
        self.lower = lower
        self.upper = upper
        self.step = step
        self.executeObjectiveTree() 
        self.zeroErrorSolution = []
        self.zeroErrorSolutionHashs = []
        self.initializeStatistics()
        self.prepareLogDirectory("logs/")
        sys.exit()
    
    def prepareLogDirectory(self, folderPath):
        directory = os.path.dirname(folderPath)
        # if directory does not exit, create it
        if not os.path.exists(directory):
            os.makedirs(directory)
        # if exists, try to clean any old log files inside it
        else: 
            for myFile in os.listdir(folderPath):
                filePath = os.path.join(folder, myFile)
            try:
                if os.path.isfile(filePath):
                    os.unlink(filePath)
            except Exception as e:
                pass

    def executeObjectiveTree(self):
        objectiveRootNode = ExpressionNode(self.objective[0])
        for i in range(len(self.objective)-1):
            objectiveRootNode.addChild(self.objective[i+1])
        testValue = self.lower
        self.y_true = []
        while testValue <= self.upper:
            objectiveResult = objectiveRootNode.execute({'x':testValue})
            self.y_true.append(objectiveResult)
            testValue += self.step

    def initializeStatistics(self):
        self.statistics = {}
        self.statistics["bestSolution"] = None
        self.statistics["bestError"] = -sys.maxint
        self.statistics["iterations"] = 0

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

        #if mse > self.bestSolutionSoFar[1]:
        if mse > self.statistics["bestError"] :
            #self.bestSolutionSoFar = (partialSolution, mse)
            self.statistics["bestError"] = mse
            self.statistics["bestSolution"] = partialSolution

        self.logExpression(self.statistics["bestSolution"])
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
        testValue = self.lower
        while testValue <= self.upper:
            expressionResult = rootNode.execute({"x":testValue})
            y_pred.append(expressionResult)
            testValue += self.step
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
        for name, c in components.iteritems():
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

    def logExpression(self, expression):
        self.statistics["iterations"] +=1
        if self.statistics["iterations"] % 100 == 0:
            self.logSearch()
            y_pred = self.buildAndExecuteTree(expression)
            with open('logs/iter'+str(self.statistics["iterations"]/100)+'.csv', 'w') as f:
                f.write("\n".join([str(x)+" "+str(fx) for x, fx in zip(np.arange(self.lower, self.upper+self.step, self.step), y_pred)]))

    def logSearch(self):
        stats = self.statistics
        with open("logs/search", "a") as myfile:
            myfile.write(", ".join([str(stats["iterations"]), str(stats["bestError"])]))
            myfile.write("\n")

    
