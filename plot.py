#! /usr/bin/env python

import csv
import sys
import matplotlib.pyplot as plt 
import numpy as np
from Utility.Utility import getFilesFromDirectory 

def parseExpressionFile(fileName):
    x, fx = [], []
    with open(fileName,'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=' ')
        # 1st line has the expression
        expression = " ".join(next(lines))
        # 2nd line has the MSE
        mse = next(lines)[0]
        # from 3rd line is f, f(x)
        for row in lines:
            x.append(row[0])
            fx.append(row[1])
        return (expression, mse, x, fx)

def fetchObjective(folderPath):
    files = getFilesFromDirectory(folderPath)
    objective = None
    for fileName in files:
        if "objective" in fileName:
            objective = parseExpressionFile(fileName)
    if objective == None:
        raise ValueError('Could not find objective.csv file')
    return objective

def fetchExpressions(folderPath):
    files = getFilesFromDirectory(folderPath)
    expressions = {}
    for fileName in files:
        with open(fileName,'r') as csvfile:
            #using substring to get ITERATION from /path/path/ITERATION.csv
            it = fileName[fileName.rfind("/")+1:fileName.rfind(".csv")]
            expressions[int(it)] = parseExpressionFile(fileName)
    return expressions

def plotAll(data):
    labels = []
    jet = plt.cm.jet
    colors = jet(np.linspace(0, 1, len(data)))
    iterations = sorted(data.keys())   

    for it, color in zip(iterations, colors):
        expressionInfo = data[it]
        expression = expressionInfo[0]
        mse = expressionInfo[1]
        x = expressionInfo[2]
        fx = expressionInfo[3]
        labels.append(str(it)+" - "+expression+" (MSE: "+str(mse)+")")
        plt.plot(x, fx, color=color)
    
    plt.xlabel('Iterations')
    plt.ylabel('Error')
    plt.legend(tuple(labels), loc='upper left') 
    plt.grid(True)
    plt.show()

def plotTwoByTwo(data, objective):
    objectiveLabel = "Objective "+objective[0]
    figureIndex = 321

    for iteration, expressionInfo in sorted(data.items()):
        plt.subplot(figureIndex)
        expression = expressionInfo[0]
        mse = expressionInfo[1]
        x = expressionInfo[2]
        fx = expressionInfo[3]
        exprLabel = str(iteration)+": "+expression+" (MSE: "+str(mse)+")"
        plt.xlabel('Iterations')
        plt.ylabel('Error')
        plt.plot(x, fx)
        plt.plot(objective[2], objective[3])
        plt.legend((objectiveLabel, exprLabel), loc='upper left') 
        plt.grid(True)
        figureIndex += 1
        if figureIndex >= 327:
            plt.show()
            figureIndex = 321
        
    plt.show()

def plotSearchStep():
    x, fx = [], []
    with open("logs/search.csv",'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=' ')
        expression = " ".join(next(lines))
        for row in lines:
            x.append(row[0])
            fx.append(row[1])
    plt.step(x, fx, where='post')
    plt.title("Search Progression")
    plt.show()

def main(args):
    expr = fetchExpressions("logs/iterations")
    objective = fetchObjective("logs/")    
    
    plotSearchStep()
    
    plotTwoByTwo(expr, objective)

    expr["Objective"] = objective
    plotAll(expr)

if __name__ == '__main__':
    main(sys.argv[1:])


