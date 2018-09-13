from Node import *
from sympy import sympify

class MCTS(object):

    def __init__(self, objective_expr="x^2 + 4*x + 1", total_iterations = 1000):
        self.objective_expr = sympify(objective_expr)
        self.total_iterations = total_iterations
        self.root = Node()
        self.root.objective = self.objective_expr
        self.iterationBreak = 1500

    def run(self):
        
        for it in range(self.total_iterations): 
            if (it+1) % self.iterationBreak == 0:
                print("Best child: ")
                print(self.root.bestChild().value)
                mynode = self.root.bestChild()
                self.root = Node(None, mynode.value)
                #self.root.value = mynode.value
                self.root.objective = self.objective_expr
                #self.root = self.root.bestChild()
            self.root.iteration()
            if self.root.highest_reward[0] == 0:
                break
        print(self.root.highest_reward)
