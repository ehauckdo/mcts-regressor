import random
import sys
import math
from ProductionRules import *
from sympy import symbols, sympify, oo, zoo, nan
from sklearn.metrics import mean_squared_error

height = 2
log = False

class NodeNew(object):

    def __init__(self, parent=None, value=1):
        self.parent = parent
        self.value = value
        self.depth = 0 if parent == None else parent.depth + 1

        if parent != None:
            self.objective = parent.objective

        # MCTS related fields
        self.visits = 0;
        self.reward = 0;
        self.C = math.sqrt(2)
        self.bounds = [sys.maxint, -sys.maxint]
        self.fullyExpanded = False

    def iteration(self):
        node = self.treePolicy()
        score = node.rollOut()
        node.backup(score)

    def treePolicy(self):
        selected_node = self

        while selected_node.depth < max_height:
            if selected_node.fullyExpanded is False:
                #print_log("Expanding node "+selected_node.value, log)
                selected_node = selected_node.expand()
                print_log("Expansion selected "+selected_node.value, log)
                return selected_node
                pass
            else:
                selected_node = selected_node.uct()
        return selected_node

    def uct(self):
        selected_node = self
        best_value = -sys.maxint

        print_log("Calculating UCT from node "+selected_node.value+", with depth "+str(selected_node.depth), log)

        for key in self.children.keys():
            child_node = self.children[key]


            total_reward = child_node.reward
            child_value = total_reward / child_node.visits
            child_value = normalize(child_value, self.bounds[0], self.bounds[1])
            print_log("Bounds: "+str(self.bounds[0])+", "+str(self.bounds[1]), log)
            print_log("Checking child "+child_node.value+", visits in this node: "+str(child_node.visits)+", raw_reward: "+str(child_node.reward)+", normalized_reward: "+str(child_value), log)

            uct_value = child_value + self.C * math.sqrt(math.log(self.visits) / child_node.visits)

            uct_value = uct_value # apply some noise here to break ties

            if uct_value > best_value:
                selected_node = child_node
                best_value = uct_value

        if selected_node == None:
            raise ValueError('No node was selected in UCT')

        #print("Selected node by UCT: "+selected_node.value)
        return selected_node


    def expand(self):
        return

    def rollOut(self):
        return

    def backup(self, reward):
        return
