import random
import sys
import math
from ProductionRules import *
from sympy import symbols, sympify, oo, zoo, nan
from sklearn.metrics import mean_squared_error

max_height = 3
log = False 

class Node(object):
    
    def __init__(self, parent=None, value="E"):
        self.parent = parent
        self.value = value
        self.depth = 0 if parent == None else parent.depth + 1
        self.highest_reward = [-sys.maxint, None]
        
        if parent != None:
            self.objective = parent.objective
    
        # MCTS related fields
        self.visits = 0;
        self.reward = 0;
        self.C = math.sqrt(2)
        self.bounds = [sys.maxint, -sys.maxint]
        self.fullyExpanded = False
        self.initializeChildren()
    
    def initializeChildren(self):
        print_log("Possible children for the current node ("+self.value+", depth "+str(self.depth)+"): ", log) 
        self.children = {};
        # check if there's E expressions, set those to expand
        if self.value.find("E") != -1:
            term = "E"
        # otherwise, check if there's I expressions, set those to expand
        elif self.value.find("I") != -1:
            term = "I"
        else:
            # if there's no expessions to be expanded, do not initialize children 
            if log:
                print_log("None", log)
            return

        # each child has the key of (Expression_Index_Position, Production_Rule_Applied)
        indexes = list([pos for pos, char in enumerate(self.value) if char == term])
        for index in indexes:
            for item in production_rules[term]:
                self.children[(index, item)] = None
       
         
        for child in self.children: print_log(child, log)

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
        # expand the tree
        #print("Children: "+str(self.children))
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

    def rollOut(self):
        # execute rollout and return Reward
        #print("Executing rollout for the expression "+self.value)
        current_depth = self.depth
        current_expr = self.value
        old_expr = ""
        
        while current_depth < self.depth+1: #and current_expr != old_expr:
            old_expr = current_expr
            current_expr = expandExpressionRandomly(current_expr)
            current_depth += 1

        print_log("Expression before Terminals: "+current_expr, log)
        current_expr = substituteAllTerms(current_expr)
        print_log("Expression after Terminals: "+current_expr, log)
        print_log("Rollouted expression: "+current_expr, log)
        #raw_input("...")

        sympy_expr = sympify(current_expr)

        #print(sympy_expr)
        y_pred = []
        y_true = []

        test_value = -10
        while test_value <= 10:
            value = sympy_expr.subs({'x':test_value})
            #try:
                #print("%.2f, %.2f, " % (sympy_expr.subs({'x':test_value}), objective.subs({'x':test_value})))
            # if found division by zero, ignore
            #except ValueError:
            #    pass
            y_pred.append(sympy_expr.subs({'x':test_value}))
            y_true.append(self.objective.subs({'x':test_value}))
            test_value += 0.5


        mse = mean_squared_error(y_true, y_pred)
        mse = -mse
        reward = [mse, sympy_expr]
        #if mse == 0:
        #    reward = [1, sympy_expr]
        #else:
        #    reward = [1/mse, sympy_expr]
        print_log("Reward from rollout: "+str(reward), log)
        #try:
        #    reward = [1/mse, sympy_expr]
        #except:
        #    print("Found reward one!")
        #    reward = [1, sympy_expr]
        #reward = random.random()
        return reward 

    def backup(self, reward):
        # update all nodes up to the root
        node = self
        print_log("Backing up reward.", log)
        while node != None:
            if reward[0] > node.highest_reward[0]:
                node.highest_reward[0] = reward[0]
                node.highest_reward[1] = reward[1]

            if reward[0] < node.bounds[0]:
                node.bounds[0] = reward[0]  
            if reward[0] > node.bounds[1]:
                node.bounds[1] = reward[0]
            print_log("Updated bounds in node "+str(node.value)+": "+str(node.bounds[0])+", "+str(node.bounds[1]), log)
            node.visits += 1
            node.reward += reward[0]
            # do we normalize the reward...?
            node = node.parent
        return None

    def bestChild(self):
        best_child = None
        most_visits = 0
        for key in self.children.keys():
            if self.children[key] == None:
                continue 
            if self.children[key].visits > most_visits:
                best_child = self.children[key]
                most_visits = self.children[key].visits

        return self if best_child == None else best_child

