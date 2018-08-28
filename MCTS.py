from Node import *
from sympy import sympify

class MCTS(object):

    def __init__(self, objective_expr="x^2 + 4*x + 1", total_iterations = 1000):
        self.objective_expr = sympify(objective_expr)
        self.total_iterations = total_iterations
        self.root = Node()
        self.root.objective = self.objective_expr

    def run(self):
        for it in range(self.total_iterations):
            self.root.iteration()
            if self.root.highest_reward[0] == 0:
                break
        print(self.root.highest_reward)
