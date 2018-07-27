import random
import sys
import math
from sympy import symbols, sympify, oo, zoo, nan
from sklearn.metrics import mean_squared_error

objective = sympify("x^2 + 4*x + 1")
#print(objective)
production_rules = { "E": ["(E + E)", "(E - E)", "(E / E)", "(E * E)", "(E ^ I)", "sin(E)", "x", "I"],
                     "I": [ 1, 2]}
max_height = 5

class Node(object):
    
    def __init__(self, parent=None, value="E"):
        self.parent = parent
        self.value = value
        self.depth = 0 if parent == None else parent.depth + 1
        
        # MCTS related fields
        self.visits = 0;
        self.reward = 0;
        self.C = math.sqrt(2)
        self.bounds = [sys.maxint, -sys.maxint]
        self.fullyExpanded = False
        self.initializeChildren()
    
    def initializeChildren(self):
        self.children = {};
        # check if there's E expressions, set those to expand
        if self.value.find("E") != -1:
            term = "E"
        # otherwise, check if there's I expressions, set those to expand
        elif self.value.find("I") != -1:
            term = "I"
        else:
            # if there's no expessions to be expanded, do not initialize children 
            return

        # each child has the key of (Expression_Index_Position, Production_Rule_Applied)
        indexes = list([pos for pos, char in enumerate(self.value) if char == term])
        for index in indexes:
            for item in production_rules[term]:
                self.children[(index, item)] = None
        
        #print("Possible children for the current node: ") 
        #for child in self.children: print(child)
        
    def iteration(self):
        node = self.treePolicy()
        score = node.rollOut()
        node.backup(score)

    def treePolicy(self):
        selected_node = self

        while selected_node.depth < max_height:
            if selected_node.fullyExpanded is False:
                print("Expanding node "+selected_node.value)
                selected_node = selected_node.expand()
                print("Expansion selected "+selected_node.value)
                return selected_node
                pass
            else:
                selected_node = selected_node.uct()
        return selected_node

    def uct(self):
        selected_node = self
        best_value = -sys.maxint 
    
        for key in self.children.keys():
            child_node = self.children[key]
            total_reward = child_node.reward
            child_value = total_reward / child_node.visits

            uct_value = child_value + self.C * math.sqrt(math.log(self.visits) / child_node.visits)
            
            uct_value = uct_value # apply some noise here to break ties

            if uct_value > best_value:
                selected_node = child_node
                best_value = uct_value

        if selected_node == None:
            raise ValueError('No node was selected in UCT')
    
        print("Selected node by UCT: "+selected_node.value)
        return selected_node

    # OK
    def expand(self):
        # expand the tree
        print("Children: "+str(self.children))
        possible_expansions = [k for k,v in self.children.items() if v == None]
        if len(possible_expansions) == 0:
            return self # must find a way to ignore explored branches!!
        
        #print("Possible expansions for the current node: ")
        #for item in possible_expansions: print(item)
        selected_expansion = random.choice(possible_expansions)
        #print("Selected expansion: "+str(selected_expansion))
        index = selected_expansion[0]
        term = selected_expansion[1]
        new_expression = self.value[:index] + str(term) + self.value[index + 1:]
        #print("New Expression after expansion: "+new_expression)
        new_node = Node(self, new_expression) 
        self.children[selected_expansion] = new_node

        if len(possible_expansions) == 1:
            self.fullyExpanded = True

        return self.children[selected_expansion]

    # OK?
    def rollOut(self):
        # execute rollout and return Reward
        print("Executing rollout for the expression "+self.value)
        current_depth = self.depth
        current_expr = self.value
        old_expr = ""
        
        while current_depth < max_height and current_expr != old_expr:
            old_expr = current_expr
            current_expr = self.expandExpressionRandomly(current_expr)
            current_depth += 1

        #print("Expression before Terminals: "+current_expr)
        current_expr = self.substituteAllTerms(current_expr)
        #print("Expression after Terminals: "+current_expr)
        print("Rollouted expression: "+current_expr)

        symbol = symbols('x') # find a way to parse all the symbols in expr!!
        sympy_expr = sympify(current_expr)

        print(sympy_expr)
        y_pred = []
        y_true = []

        test_value = -10
        while test_value <= 10:
            value = sympy_expr.subs({'x':test_value})
            try:
                print("%.2f, %.2f" % (sympy_expr.subs({'x':test_value}), objective.subs({'x':test_value}))) 
            # if found division by zero, ignore
            except ValueError:
                pass
            y_pred.append(sympy_expr.subs({'x':test_value}))
            y_true.append(objective.subs({'x':test_value}))
            test_value += 0.5


        mse = mean_squared_error(y_true, y_pred)
        reward = mse
        #reward = random.random()

        #print("Reward: "+str(reward))
        if reward < self.bounds[0]:
            self.bounds[0] = reward    
        elif reward > self.bounds[1]:
            self.bounds[1] = reward

        return reward 

    def backup(self, reward):
        # update all nodes up to the root
        node = self
        while node != None:
            node.visits += 1
            node.reward += reward
            # do we normalize the reward...?
            node = node.parent
        return None


    def expandExpressionRandomly(self, expr):
        #print("Expression to be expanded: "+ expr)
        indexes = list([pos for pos, char in enumerate(expr) if char == "E"])
        if len(indexes) == 0:
            return expr
        #print("indexes of Es: "+ str(indexes))
        chosen_index = random.choice(indexes)
        #print("Chosen index: " + str(chosen_index))
        chosen_production_rule = random.choice(production_rules["E"])
        #print("Chosen production rule: "+ str(chosen_production_rule))
        new_expr = expr[:chosen_index] + str(chosen_production_rule) + expr[chosen_index + 1:]
        #print("New expression: "+new_expr)
        return new_expr

    def expandExpression(self, expr, pr, term):
        #print("Expression to be expanded: "+ expr)
        indexes = list([pos for pos, char in enumerate(expr) if char == term])
        if len(indexes) == 0:
            return expr
        #print("indexes of Es: "+ str(indexes))
        chosen_index = random.choice(indexes)
        #print("Chosen index: " + str(chosen_index))
        chosen_production_rule = random.choice(pr[term])
        #print("Chosen production rule: "+ str(chosen_production_rule))
        new_expr = expr[:chosen_index] + str(chosen_production_rule) + expr[chosen_index + 1:]
        #print("New expression: "+new_expr)
        return new_expr

    def substituteAllTerms(self, expr):
        expr = expr.replace("E", "I")
        index = expr.find("I")
        while index != -1:
            chosen_production_rule = random.choice(production_rules["I"])
            expr = expr[:index] + str(chosen_production_rule) + expr[index + 1:]
            index = expr.find("I")

        return expr

