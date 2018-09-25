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


components = [ExpressionComponent(1, 0),
                ExpressionComponent(2, 0),
                ExpressionComponent(0, 0),
                ExpressionComponent("x", 0),
                ExpressionComponent(np.add, 2),
                ExpressionComponent(np.subtract, 2),
                ExpressionComponent(np.multiply, 2),
                ExpressionComponent(safediv, 2),
                ExpressionComponent(np.sin, 1)
                #ExpressionComponent(__add__, 2),
                #ExpressionComponent(__sub__,2),
                #ExpressionComponent(__mul__, 2),
                #ExpressionComponent(math.pow, 2),
                ]

