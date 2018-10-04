#! /usr/bin/env python

# importing the required module 
import matplotlib.pyplot as plt 
import csv
import sys
from Utility.Utility import getFilesFromDirectory 
   
styles = ['-', '--', '-.', ':',',', 'o', 'v', '^']
s = 0

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

def plotChart(fileName):
    global s
    x = []
    y = []
    with open(fileName,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=' ')
        expression = " ".join(next(plots))
        mse = next(plots)[0]
        for row in plots:
            x.append(row[0])
            y.append(row[1])
    plt.plot(x, y, styles[s])
    s = 0 if s >= 3 else s + 1
    fileName = fileName[fileName.find('/')+1:]
    return fileName+"(MSE:"+mse+"): "+expression

def plotTwoByTwo(data, objective):
    labels = []
    objectiveLabel = "Objective "+" (MSE: "+str(objective[1])+")"+objective[0]
    labels.append(objectiveLabel)
    figureIndex = 521

    for iteration, expressionInfo in sorted(data.items()):
        plt.subplot(figureIndex)
        expression = expressionInfo[0]
        mse = expressionInfo[1]
        x = expressionInfo[2]
        fx = expressionInfo[3]
        exprLabel = str(iteration)+" (MSE: "+str(mse)+")"+expression
        labels.append(str(iteration)+" (MSE: "+str(mse)+")"+expression)
        plt.xlabel('Iterations')
        plt.ylabel('Error')
        plt.plot(x, fx)
        plt.plot(objective[2], objective[3])
        plt.legend((objectiveLabel, exprLabel), loc='upper left') 
        plt.grid(True)
        figureIndex += 1
        
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
    for key, value in sorted(expr.items()):
        print key
        print value
    
    objective = fetchObjective("logs/")    
    print objective

    plotSearchStep()

    plotTwoByTwo(expr, objective)

if __name__ == '__main__':
    main(sys.argv[1:])


