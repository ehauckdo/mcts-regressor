import random
import copy
from sklearn.metrics import mean_squared_error
import numpy as np
import math
from ExpressionComponents import * 
from ExpressionNode import *

class SolutionHandler(object):
    def __init__(self):
        self.objective = None 
        self.expansion_limit = 0

    def addComponent(self, component):
        self.value.append(component)

    def getAvailableExpansions(self):
        return expansions

    def getNumberExpansionsPossible(self):
        return 0

    def expandSolution(self):
        return

    def getReward(self, valueHolder):
        return 0

    def getChildren(self, valueHolder):
        return 0

    def clear(self):
        self.value = {}
