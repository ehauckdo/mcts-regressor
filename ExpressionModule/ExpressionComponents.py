from __future__ import division
import inspect
import numpy as np
import math
import logging

class ExpressionComponent(object):

    def __init__(self, value, arity):
        self.value = value
        self.arity = arity

    def __str__(self):
        return str(self.value)+" - "+str(self.arity)

    def __hash__(self):
        return hash(str(self))

def div(x, y):
    if y == 0: return 0
    return x/y

def ln(x):
    if x <= 0: return 0
    return np.log(x)
   
def pow(x, y):
    if x < 0 and int(y) != y:
        x = abs(x)
    if x == 0 and y < 0:
       return 0
    if int(x) == x and int(y) == y and y < 0:
        y = float(y)
    return np.power(x, y)

def initializeComponentVariables(numberVar):
    if numberVar > 26:
         raise ValueError("Expressions with more than 26 variables are not currently acceptable")
    variables = []
    indexes = np.arange(ord('x'), ord('x')+numberVar)
    indexes = [i - 26 if i > ord('z') else i for i in indexes]    
    for i in indexes:
        var = chr(i)
        variables.append(var)
        component = ExpressionComponent(var, 0) 
        components[var] = component
        components_reversed[str(component)] = var   
    return variables    

components = {  "0" : ExpressionComponent(0, 0),
                "1" : ExpressionComponent(1, 0),
                "2" : ExpressionComponent(2, 0),
                "add": ExpressionComponent(np.add, 2),
                "sub": ExpressionComponent(np.subtract, 2),
                "mul": ExpressionComponent(np.multiply, 2),
                "div": ExpressionComponent(np.true_divide, 2),
                "cos": ExpressionComponent(np.cos, 1),
                "sin": ExpressionComponent(np.sin, 1),
                "pow": ExpressionComponent(np.power, 2),
                "ln": ExpressionComponent(np.log, 1)
                }

# a reverse mapping to facilitate readable expression constrution
components_reversed = {str(v): k for k, v in components.iteritems()}
