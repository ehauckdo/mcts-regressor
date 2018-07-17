import random

operators = ["+", "-"]
terminals = [1, "x"]
max_height = 5

class Node(object):
    
    def __init__(self):
        self.value = []
        self.terminals = 0
        self.operators = 0

        self.visits = 0;
        self.reward = 0;
        self.fullyExpanded = False
        self.children = None;
        self.rollOut()

    def iteration(self):
        node = treePolicy()

    def treePolicy(self):
        # selected a node from the tree to expand
        return self

    def rollOut(self):
        # execute rollout and return Reward
        rollout_stack = list(self.value)
        rollout_terminals = self.terminals
        rollout_operators = self.operators

        while len(rollout_stack) < max_height:
            if rollout_operators >= max_height/2:
                self.pushTerminal(rollout_stack)
                rollout_terminals += 1
            else:
                term = self.pushAny(rollout_stack)
                if term in terminals:
                    rollout_terminals += 1
                else:
                    rollout_operators += 1

            print("rollout_stack: ", rollout_stack) 
            print("number of terminals", rollout_terminals) 
            print("number of operators: ", rollout_operators) 

        return 0

    def backup(self, node, reward):
        # update all nodes up to the root
        return None

    def expand(self):
        if self.fullyExpanded != True:
            # expand the tree
            return

    def pushTerminal(self, stack):
        term = random.choice(terminals)
        stack.append(term)
        return term

    def pushOperator(self, stack):
        term = random.choice(operators)
        stack.append(term)
        return term

    def pushAny(self, stack):
        candidates = operators + terminals 
        term = random.choice(candidates)
        stack.append(term)
        return term
