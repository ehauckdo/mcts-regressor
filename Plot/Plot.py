import csv
import sys
import matplotlib.pyplot as plt
import numpy as np
from Utility.Utility import prepareLogDirectory, getFilesFromDirectory

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

def plotAll(data, objective, plots=0.5):
    labels = []
    iterationKey = sorted(data.keys())
    selectedKeys = np.linspace(1, len(iterationKey)-1, len(iterationKey)*plots, dtype=int)
    jet = plt.cm.jet
    colors = jet(np.linspace(0, 1, (len(iterationKey)*plots)+1))

    for key, color in zip(selectedKeys, colors):
        expressionInfo = data[iterationKey[key]]
        expression = expressionInfo[0]
        mse = expressionInfo[1]
        x = expressionInfo[2]
        fx = expressionInfo[3]
        labels.append(str(key)+" - "+expression+" (MSE: "+str(mse)+")")
        plt.plot(x, fx, color=color)

    labels.append(objective[0])
    plt.plot(objective[2],objective[3],'--')

    plt.xlabel('Iterations')
    plt.ylabel('Error')
    plt.legend(tuple(labels), loc='upper left')
    plt.grid(True)
    displayAndSave("All_Functions"+"_".join(objective[0].split()))

def plotTwoByTwo(data, objective):
    objectiveLabel = "Objective "+objective[0]
    figureIndex = 321
    fileNameIndex = 1

    for iteration, expressionInfo in sorted(data.items()):
        plt.subplot(figureIndex)
        plt.xlabel('Iterations')
        plt.ylabel('Error')
        plt.plot(objective[2], objective[3], '--')
        expression = expressionInfo[0]
        mse = expressionInfo[1]
        x = expressionInfo[2]
        fx = expressionInfo[3]
        plt.plot(x, fx)
        exprLabel = str(iteration)+": "+expression+" (MSE: "+str(mse)+")"
        plt.legend((objectiveLabel, exprLabel), loc='upper left')
        plt.grid(True)
        figureIndex += 1
        if figureIndex >= 327:
            displayAndSave("Two_by_two_"+str(fileNameIndex))
            figureIndex = 321
            fileNameIndex += 1
    if figureIndex > 321:
        displayAndSave("Two_by_two_"+str(fileNameIndex))

def boxplot(logFolders):
    functionStats = {}

    figureIndex = 101
    for f in logFolders:
        figureIndex += 10

    for function in logFolders:
        functionStats[function] = {}
        functionStats[function]["BestMSE"] = []
        executionLogFolders = getFilesFromDirectory(function)
        for executionLog in executionLogFolders:
            logFiles = getFilesFromDirectory(executionLog)
            for fileName in logFiles:
                if "iterations" in fileName:
                    bestError = 100000.0
                    results = []
                    iterations = getFilesFromDirectory(fileName)
                    for iters in iterations:
                        with open(iters,'r') as csvfile:
                            lines = csv.reader(csvfile, delimiter=' ')
                            expression = next(lines, None)
                            mse = float(next(lines, None)[0])
                            if mse < bestError:
                                bestError = mse
                                for row in lines:
                                    variables = row[0]
                                    fx = row[-1]
                if "search" in fileName:
                    mse = 0
                    with open(fileName,'r') as csvfile:
                        lines = csv.reader(csvfile, delimiter=' ')
                        for row in lines:
                            mse = row[1]
                            pass
                    if float(mse) < 50000.0:
                        functionStats[function]["BestMSE"].append(mse)
        functionStats[function]["BestMSE"] = [float(x) for x in functionStats[function]["BestMSE"]]

        plt.subplot(figureIndex)
        plt.boxplot(functionStats[function]["BestMSE"])

        plt.xlabel(function)
        plt.ylabel('Error')
        plt.grid(True)
        figureIndex += 1
    plt.show()


def displayAndSave(fileName):
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show(block=False)
    plt.savefig("figs/"+fileName)
    plt.close()

def plotSearchStep():
    x, fx = [], []
    with open("logs/search.csv",'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=' ')
        expression = " ".join(next(lines))
        for row in lines:
            x.append(row[0])
            fx.append(row[1])
    plt.step(x, fx, where='post')
    plt.grid(True)
    plt.title("Search Progression")
    displayAndSave("SearchProgress")

