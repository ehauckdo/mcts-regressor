import logging
from numpy import nan

class ExpressionNode(object):

    def __init__(self, component):
        self.value = component.value
        self.arity = component.arity
        self.children = []
        for i in range(component.arity):
            self.children.append(None)

    def addChild(self, component):
        node = ExpressionNode(component)
        for i in range(len(self.children)):
            if self.children[i] != None:
                success = self.children[i].addChild(component)
                if success:
                    return True
            else:
                self.children[i] = node
                return True
        return False

    def execute(self, variables={}):
        returnValue = None
   
        try:
            if self.arity == 0:
                if self.value in variables.keys():
                    returnValue = variables[self.value]
                    #return variables[self.value]
                elif self.value == "x":
                    raise ValueError("Variable was not converted to a number during execution")
                else:
                    returnValue = self.value
                    #return self.value

            if self.arity == 1:
                returnValue = self.value(self.children[0].execute(variables))
                #return self.value(self.children[0].execute(variables))

            if self.arity == 2:
                returnValue = self.value(self.children[0].execute(variables), self.children[1].execute(variables))
                #return self.value(self.children[0].execute(variables), self.children[1].execute(variables))
        
        except:
            returnValue = nan
          

        return returnValue

