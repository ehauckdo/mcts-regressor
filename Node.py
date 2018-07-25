import random
from sympy import symbols

production_rules = { "E": ["(E + E)", "(E - E)", "(E / E)", "(E * E)", "(E ^ I)", "sin(E)", "I"],
                     "I": ["x", 1, 2]}
max_height = 5

class Node(object):
    
    def __init__(self, parent=None, value="E"):
        self.parent = parent
        self.value = value
        self.depth = 0 if parent == None else parent.depth + 1
        
        # MCTS related fields
        self.visits = 0;
        self.reward = 0;
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

        if self.fullyExpanded is False:
            selected_node = self.expand()
            pass
        else:
            #call uct
            pass    
        return selected_node

    # OK
    def expand(self):
        # expand the tree
        possible_expansions = [k for k,v in self.children.items() if v == None]
        if len(possible_expansions) == 0:
            return

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

        return 0

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

