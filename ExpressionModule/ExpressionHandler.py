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
from Utility.Utility import prepareLogDirectory

class ExpressionHandler(SolutionHandler):

    def __init__(self, objective=None, lower=-10, upper=10, step=41):
        self.objective = objective
        self.partialSolution = []
        self.maxSolutionSize = 5 
        self.lower = lower
        self.upper = upper
        self.step = step
        self.zeroErrorSolution = []
        self.zeroErrorSolutionHashs = []
        self.initializeStatistics()
        prepareLogDirectory("logs/")
        prepareLogDirectory("logs/iterations/")
        self.y_true = self.executeTree(self.buildTree(objective)) 
        self.logExpression(objective, "objective.csv")

    def initializeStatistics(self):
        self.statistics = {}
        self.statistics["bestSolution"] = None
        self.statistics["bestError"] = sys.maxint
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
        mse = sys.maxint if np.isinf(mse) else mse
        mse = -sys.maxint if np.isneginf(mse) else mse      
        
        self.statistics["iterations"] +=1

        if (mse < self.statistics["bestError"] or 
           (mse == self.statistics["bestError"] and len(partialSolution) < len(self.statistics["bestSolution"]))):
            self.statistics["bestError"] = mse
            self.statistics["bestSolution"] = partialSolution
            self.logSearch()
            self.logExpression(self.statistics["bestSolution"], "iterations/"+str(self.statistics["iterations"])+".csv")
        
        if mse == 0:
            solutionHash = hash(tuple(partialSolution))
            logging.info("0 error solution found! Hash: "+str(solutionHash))
            if solutionHash not in self.zeroErrorSolutionHashs:
                self.zeroErrorSolution.append(partialSolution)
                self.zeroErrorSolutionHashs.append(solutionHash)
        #else:
        #    mse = -mse

        #logging.info("Expression Result for x=5: "+str(rootNode.execute({"x":5})))
        #logging.info("Objective Result for x=5: "+str(objectiveRootNode.execute({"x":5})))
        reward = 1 /(1+mse)            

        return reward

    def getMSE(self, partialSolution):
        rootNode = self.buildTree(partialSolution)
        y_pred = self.executeTree(rootNode)
        logging.info(y_pred)
        if (np.isnan(y_pred).any()):
            logging.info("Returning maxint")
            return sys.maxint
        #y_pred = np.nan_to_num(y_pred)
        y_pred = np.clip(y_pred, -sys.maxint, sys.maxint)
        #y_pred[np.isinf(y_pred)] = sys.maxint
        #y_pred[np.isneginf(y_pred)] = -sys.maxint
        logging.info(y_pred)
        mse = mean_squared_error(self.y_true, y_pred)
        return mse
    
    def buildTree(self, partialSolution):
        rootNode = ExpressionNode(partialSolution[0])
        for i in range(len(partialSolution)-1):
            logging.debug("Adding child: "+str(partialSolution[i+1].value))
            rootNode.addChild(partialSolution[i+1])
        return rootNode  

    def executeTree(self, rootNode):
        y_pred = []
        testValues = np.linspace(self.lower, self.upper, self.step)
        for v in testValues:
            expressionResult = rootNode.execute({"x":v})
            y_pred.append(expressionResult)
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
            try:
                component = partialSolution[i].value.__name__
            except:
                component = str(partialSolution[i].value)
            string.append(component)
        return string

    def logExpression(self, expression, fileName="loggedExpression.csv"):
        rootNode = self.buildTree(expression)
        y_pred = self.executeTree(rootNode)
        mse = self.getMSE(expression)
        with open('logs/'+fileName, 'w') as f:
            f.write(" ".join(self.printExpression(expression))+"\n")
            f.write("{0:.2f}".format(mse)+"\n")
            f.write("\n".join([str(x)+" "+str(fx) for x, fx in zip(np.linspace(self.lower, self.upper, self.step), y_pred)]))

    def logSearch(self):
        stats = self.statistics
        with open("logs/search.csv", "a") as myfile:
            myfile.write(" ".join([str(stats["iterations"]), "{0:.2f}".format(stats["bestError"])]))
            myfile.write("\n")

    
