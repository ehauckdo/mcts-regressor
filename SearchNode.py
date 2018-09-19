from SolutionHandler import SolutionHandler
from Utility import print_log, normalize
import copy
import sys
import random
import math

logging = True

class SearchNode(object):

    def __init__(self, handler=SolutionHandler(), parent=None, value=[]):
        random.seed(0)
        self.value = value
        self.parent = parent
        self.handler = handler
        self.visits = 0   
        self.reward = 0
        self.depth_limit = 5
        self.C = math.sqrt(2)     
        self.depth = 0 if parent == None else parent.depth + 1    
        self.bounds = [sys.maxint, -sys.maxint]
        self.fullyExpanded = False
        self.initChildren()        

        #print_log("Handler objective: ",logging)
        #self.handler.printValue(handler.objective)

        #for i in range(20): 
        #    self.handler.expandSolution(self.value)
        #    print_log("len: "+str(len(self.value))+", value: ",logging)
        #    self.handler.printValue(self.value)
        #    print_log("Moves lef1t:"+str(self.handler.getNumberExpansionsPossible(self.value)),logging)
        #    print_log("",logging) 
       
    def initChildren(self):
        self.children = {}  
        valueHolder = []
        current_node = self
        while ( current_node != None ):
            for value in current_node.value:
                valueHolder.append(value)
            current_node = current_node.parent
        possible_children = self.handler.getChildren(valueHolder)
        if len(possible_children) == 0:
            self.fullyExpanded = True
        for component in possible_children:
            self.children[component] = None

    def iteration(self):
        print_log("==== New Iteration ====", logging)
        self.handler.valueHolder = copy.deepcopy(self.value)
        node = self.treePolicy()
        reward = node.rollOut()
        node.backup(reward)

    def treePolicy(self):
        selected_node = self
        
        while selected_node.depth < self.depth_limit:
            if selected_node.fullyExpanded is False:
                print_log("Expanding node:",logging)
                self.handler.printValue(selected_node.value)
                selected_node = selected_node.expand()
                break
            else:
                if not selected_node.children:
                    break  
                selected_node = selected_node.uct()
        print_log("Selected node from treePolicy: ", logging)
        self.handler.printValue()
        return selected_node

    def uct(self):
        selected_node = self
        selected_node_vaue = None
        best_value = -sys.maxint

        print_log("Calculating UCT from node depth "+str(selected_node.depth), logging)
        for key in self.children.keys():
            child_node = self.children[key]
        
            total_reward = child_node.reward
            child_value = total_reward / child_node.visits

            child_value = normalize(child_value, self.bounds[0], self.bounds[1])
            #print_log("Bounds: "+str(self.bounds[0])+", "+str(self.bounds[1]), logging)

            uct_value = child_value + self.C * math.sqrt(math.log(self.visits) / child_node.visits)

            uct_value = uct_value # apply some noise here to break ties

            if uct_value > best_value:
                selected_node = child_node
                selected_node_value = key
                best_value = uct_value
        
        if selected_node == None:
            raise ValueError('No node was selected in UCT')

        self.handler.valueHolder.append(selected_node_value)
        print_log("Selected node by UCT: ",logging)
        self.handler.printValue(selected_node.value)
        return selected_node

    def expand(self):
        
        possible_expansions = []
        print_log("Children: ", logging)
        for key in self.children.keys():
            if self.children[key] == None:
                print_log(str(key)+": None", logging)
                possible_expansions.append(key)        
            else:
                print_log(str(key)+": Expanded", logging)

        chosen_expansion = random.choice(possible_expansions)
        new_child = SearchNode(self.handler, self, [chosen_expansion])
        self.children[chosen_expansion] = new_child
        self.handler.valueHolder.append(chosen_expansion)
        
        print_log("new child value: ",logging)
        self.handler.printValue(new_child.value)
        if len(possible_expansions) == 1:
            self.fullyExpanded = True
            print("FULLY EXPANDED")
        
        return new_child

    def rollOut(self):
        current_depth = self.depth
        valueHolder = copy.deepcopy(self.handler.valueHolder)
        
        while current_depth < self.depth_limit and self.handler.expandSolution(valueHolder) == True:
            #self.handler.printValue(valueHolder)
            current_depth += 1 

        reward = self.handler.getReward(valueHolder)
        print_log("Reward: "+str(reward),logging)

        return reward

    def backup(self, reward):
        node = self
        print_log("Backing up reward.", logging)
        while node != None:
            if reward < node.bounds[0]:
                node.bounds[0] = reward
            if reward > node.bounds[1]:
                node.bounds[1] = reward
            node.visits += 1
            node.reward += reward
            print_log("Updated bounds in node: "+str(node.bounds[0])+", "+str(node.bounds[1]), logging)
            node = node.parent

