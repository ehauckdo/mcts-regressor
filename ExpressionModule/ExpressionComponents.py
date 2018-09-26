from __future__ import division
import numpy as np
import math

class ExpressionComponent(object):

    def __init__(self, value, arity):
        self.value = value
        self.arity = arity

    def __str__(self):
        return str(self.value)+" - "+str(self.arity)

    def __hash__(self):
        return hash(str(self))


def safediv(x, y):
    if y == 0: return 0
    return x/y


components = {  "0" : ExpressionComponent(0, 0),
                "1" : ExpressionComponent(1, 0),
                "2" : ExpressionComponent(2, 0),
                "x" :ExpressionComponent("x", 0),
                "add": ExpressionComponent(np.add, 2),
                "sub": ExpressionComponent(np.subtract, 2),
                "mul": ExpressionComponent(np.multiply, 2),
                "div": ExpressionComponent(safediv, 2),
                "sin": ExpressionComponent(np.sin, 1)
                }

