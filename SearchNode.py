from SolutionHandler import SolutionHandler
from Utility import print_log
import copy
import sys
import random

class SearchNode(object):

    def __init__(self, handler=SolutionHandler(), parent=None):
        random.seed(0)
        self.value = []
        self.parent = parent
        self.handler = handler
        self.visits = 0   
        self.reward = 0
        self.depth_limit = 5     
        self.depth = 0 if parent == None else parent.depth + 1    
        self.bounds = [sys.maxint, -sys.maxint]
        self.fullyExpanded = False
        self.initChildren()        


        print("Handler objective: ")
        self.handler.printValue(handler.objective)
       
        self.iteration() 
        return

        #for i in range(20): 
        #    self.handler.expandSolution(self.value)
        #    print("len: "+str(len(self.value))+", value: ")
        #    self.handler.printValue(self.value)
        #    print("Moves left:"+str(self.handler.getNumberExpansionsPossible(self.value)))
        #    print("") 
       
    def initChildren(self):
        self.children = {}
        possible_children = self.handler.getChildren(self.value)
        for component in possible_children:
            self.children[component.value] = None

    def iteration(self):
        node = self.treePolicy()
        reward = node.rollOut()
        node.backup(reward)

    def treePolicy(self):
 
        return self

    def uct(self):
        return SearchNode()

    def expand(self):
        possible_expansions = []
        index = random.randint(0, len(self.children)-1)
        #while self.children[index] != None: 
        #    index = random.randint(0, len(self.children)-1)
        

    def rollOut(self):
        current_depth = self.depth
        valueHolder = copy.deepcopy(self.value)
        
        while current_depth < self.depth_limit and self.handler.expandSolution(valueHolder) == True:
            print("\nExpanded: ")
            self.handler.printValue(valueHolder)
            current_depth += 1 

        reward = self.handler.getReward(valueHolder)
        print("Reward: "+str(reward))

        return reward

    def backup(self, reward):
        node = self
        print_log("Backing up reward.", True)
        while node != None:
            if reward < node.bounds[0]:
                node.bounds[0] = reward
            if reward > node.bounds[1]:
                node.bounds[1] = reward
            node.visits += 1
            node.reward += reward
            print_log("Updated bounds in node: "+str(node.bounds[0])+", "+str(node.bounds[1]), True)
            node = node.parent
