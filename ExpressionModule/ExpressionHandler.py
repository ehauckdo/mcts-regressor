import random
import logging
import sys
import math
import os, shutil
import numpy as np
from collections import namedtuple
from sklearn.metrics import mean_squared_error
from SolutionHandler import SolutionHandler
from ExpressionModule.ExpressionNode import ExpressionNode
from ExpressionModule.ExpressionComponents import initializeComponentVariables, components, components_reversed
from Utility.Utility import prepareLogDirectory

class ExpressionHandler(SolutionHandler):

    def __init__(self, objective=None,variables=1, folder="default", lower=-10, upper=10, points=100, numberSamples=50):
        #self.objective = objective
        self.partialSolution = []
        #self.loggingDirectory = "logs/"+folder+"/" 
        self.loggingDirectory = folder 
        #prepareLogDirectory(self.loggingDirectory)
        #prepareLogDirectory(self.loggingDirectory+"iterations/")
        #logging.basicConfig(self.loggingDirectory+"/log",level=logging.INFO, filemode='w')
        self.maxSolutionSize = 5 
        self.lower = lower
        self.upper = upper
        self.points = points
        self.numberSamples = numberSamples
        self.zeroErrorSolution = []
        self.zeroErrorSolutionHashs = []
        self.initializeStatistics()
        self.variables = initializeComponentVariables(variables)
        self.initializeSamples()
        self.setObjective(objective)
        #self.y_true = self.executeTree(self.buildTree(objective)) 

    def setObjective(self, objective):
        if type(objective) is list:
            self.objective = objective
        else:
            parts = []
            for elem in objective.split():
                parts.append(components[elem])
            self.objective = parts
        self.y_true = self.executeTree(self.buildTree(self.objective))
        # if any of the samples generate nan, delete them from sample list
        for i in reversed(range(len(self.y_true))):
            if math.isnan(self.y_true[i]):
                del self.y_true[i]
                del self.samples[i]
        # if any of the samples generate infinity, clip between maxints
        self.y_true = np.clip(self.y_true, -sys.maxint, sys.maxint)
        self.logExpression(self.objective, "objective.csv", self.y_true)

    def initializeSamples(self):
        #random.seed(1)
        testValues = np.linspace(self.lower, self.upper, self.points)
        self.samples = []
        for i in range(self.numberSamples):
            sample = []
            for var in self.variables:
                sample.append(random.choice(testValues))
            self.samples.append(sample)
        logging.info(self.samples)

    def initializeStatistics(self):
        self.statistics = {}
        self.statistics["bestSolution"] = None
        self.statistics["bestError"] = np.inf #sys.maxint
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


    def getRolloutReward(self, partialSolution):
        mse = self.getMSE(partialSolution)
        
        # this is just for safety, infinities should have
        # been handled in getMSE 
        #mse = sys.maxint if np.isinf(mse) else mse
        #mse = -sys.maxint if np.isneginf(mse) else mse      
        
        self.statistics["iterations"] +=1

        if (mse < self.statistics["bestError"] or 
           (mse == self.statistics["bestError"] and len(partialSolution) < len(self.statistics["bestSolution"]))):
            self.statistics["bestError"] = mse
            self.statistics["bestSolution"] = partialSolution
            logging.info("Solution with best error found so far. Logging...")
            self.logSearch()
            self.logExpression(self.statistics["bestSolution"], "iterations/"+str(self.statistics["iterations"])+".csv")
        
        if mse == 0:
            solutionHash = hash(tuple(partialSolution))
            logging.info("0 error solution found! Hash: "+str(solutionHash))
            if solutionHash not in self.zeroErrorSolutionHashs:
                self.zeroErrorSolution.append(partialSolution)
                self.zeroErrorSolutionHashs.append(solutionHash)

        #logging.info("Expression Result for x=5: "+str(rootNode.execute({"x":5})))
        #logging.info("Objective Result for x=5: "+str(objectiveRootNode.execute({"x":5})))
        reward = 1 /(1+mse)            

        return reward

    def getMSE(self, partialSolution):
        rootNode = self.buildTree(partialSolution)
        y_pred = self.executeTree(rootNode)

        #logging.info(", ".join(["{0:.2f}".format(elem) for elem in y_pred]))
        #logging.info(y_pred)
        # if a nan is found in the function results, return biggest error possible
        if (np.isnan(y_pred).any()):
            return sys.maxint

        # if there are any infinities, we change then to max int
        y_pred = np.clip(y_pred, -sys.maxint, sys.maxint)

        #logging.info(y_pred)
        mse = mean_squared_error(self.y_true, y_pred)
        logging.info("MSE: "+str(mse))
        return mse
    
    def buildTree(self, partialSolution):
        rootNode = ExpressionNode(partialSolution[0])
        for i in range(len(partialSolution)-1):
            logging.debug("Adding child: "+str(partialSolution[i+1].value))
            rootNode.addChild(partialSolution[i+1])
        return rootNode  

    def executeTree(self, rootNode):
        y_pred = []

        # random sampling
        for sample in self.samples:
            varValues = dict(zip(self.variables, sample))
            expressionResult = rootNode.execute(varValues)
            y_pred.append(expressionResult)
            #logging.info(varValues)

        #testValues = np.linspace(self.lower, self.upper, self.points)
        # homogeneous, equally-spaced sampling
        #for v in testValues:
        #    expressionResult = rootNode.execute({"x":v})
        #    y_pred.append(expressionResult)
        
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

    def printExpression(self, partialSolution=None):
        partialSolution = partialSolution if partialSolution != None else self.partialSolution
        if len(partialSolution) == 0:
            return(["*empty*"])

        string = []
        for i in range(len(partialSolution)):
            #try:
            #    component = partialSolution[i].value.__name__
            #except:
            #    component = str(partialSolution[i].value)
            #string.append(str(partialSolution[i]))
            string.append(components_reversed[str(partialSolution[i])])
        return string

    def logExpression(self, expression, fileName="loggedExpression.csv", y_pred=None):
        if y_pred is None:
            rootNode = self.buildTree(expression)
            y_pred = self.executeTree(rootNode)
        mse = self.getMSE(expression)
        with open(self.loggingDirectory+fileName, 'w') as f:
            f.write(" ".join(self.printExpression(expression))+"\n")
            f.write("{0:.5f}".format(mse)+"\n")
            
            f.write("\n".join([' '.join([str(s) for s in x])+" "+str(fx) for x, fx in zip(self.samples, y_pred)]))

    def logSearch(self):
        stats = self.statistics
        with open(self.loggingDirectory+"search.csv", "a") as myfile:
            myfile.write(" ".join([str(stats["iterations"]), "{0:.5f}".format(stats["bestError"])]))
            myfile.write("\n")

    
