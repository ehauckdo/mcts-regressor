import copy
import sys
import random
import math
from Utility import print_log, normalize
from SolutionHandler import SolutionHandler

logging = True

class SearchNode(object):

    def __init__(self, handler=SolutionHandler(), parent=None, components=[]):
        random.seed(0)
        self.components = components
        self.parent = parent
        self.handler = handler
        self.visits = 0   
        self.reward = 0
        self.depth_limit = 5
        self.C = math.sqrt(2)     
        self.depth = 0 if parent == None else parent.depth + 1    
        self.bounds = [sys.maxint, -sys.maxint]
        self.fullyExpanded = False
        self.initChildrenList()        
       
    def initChildrenList(self):
        #print("Initializing children list...")
        self.children = {}  
        valueHolder = self.getComponentsUntilCurrentNode()
        
        #print("valueHolder: ")
        #self.handler.printComponents(valueHolder)
        
        possible_children = self.handler.getPossibleChildren(valueHolder)
        if len(possible_children) == 0:
            self.fullyExpanded = True
            #print("This node has no children")
        for component in possible_children:
            self.children[component] = None
        #print("Available children: (len: "+str(len(possible_children))+" ")
        #self.handler.printComponents(possible_children)

    def iteration(self):
        print_log("==== New Iteration ====", logging)
        self.handler.partialSolution = copy.deepcopy(self.components)
        node = self.treePolicy()
        reward = node.rollOut()
        node.backup(reward)

    def treePolicy(self):
        selected_node = self
        
        while selected_node.depth < self.depth_limit:
            if selected_node.fullyExpanded is False:
                print_log("Expanding node:",logging)
                self.handler.printComponents(selected_node.components)
                selected_node = selected_node.expand()
                break
            else:
                if not selected_node.children:
                    break  
                selected_node = selected_node.uct()
        print_log("Selected node from treePolicy: ", logging)
        self.handler.printComponents()
        return selected_node

    def uct(self):
        selected_node = self
        selected_node_value = None
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

        self.handler.partialSolution.append(selected_node_value)
        print_log("Selected node by UCT: ",logging)
        self.handler.printComponents(selected_node.components)
        return selected_node

    def expand(self):
        uninitializedChildren = self.getUninitializedChildren()

        selectedComponent = random.choice(uninitializedChildren)
        self.handler.partialSolution.append(selectedComponent)
        newChild = SearchNode(self.handler, self, [selectedComponent])
        self.children[selectedComponent] = newChild
        
        print_log("new child value: ",logging)
        self.handler.printComponents(newChild.components)
        if len(uninitializedChildren) == 1:
            self.fullyExpanded = True
            print("FULLY EXPANDED")
        
        return newChild

    def rollOut(self):
        current_depth = self.depth
        componentHolder = copy.deepcopy(self.handler.partialSolution)
        
        while current_depth < self.depth_limit and self.handler.expandSolution(componentHolder) == True:
            #self.handler.printComponents(valueHolder)
            current_depth += 1 

        reward = self.handler.getReward(componentHolder)
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

    def bestChild(self):
        print("Searching best child...")
        best_child = None
        most_visits = -1
        for key in self.children.keys():
            print("Checking key "+str(key))
            print("visits: "+str(self.children[key].visits)+", reward: "+str(self.children[key].reward))
            if self.children[key] == None:
                continue
            if self.children[key].visits > most_visits:
                best_child = self.children[key]
                most_visits = self.children[key].visits
        return best_child

    def bestBranch(self):
        print("Searching best child...")
        componentHolder = copy.deepcopy(self.components)
        current_node = self
        while len(current_node.children.keys()) != 0:
            print("Checking node depth "+str(current_node.depth))
            most_visits = -1
            for key in current_node.children.keys():
                print("Checking key "+str(key))
                print("visits: "+str(current_node.children[key].visits)+", reward: "+str(current_node.children[key].reward))
                if current_node.children[key] == None:
                    continue
                if current_node.children[key].visits > most_visits:
                    best_child = current_node.children[key]
                    most_visits = current_node.children[key].visits
            print("Selected node: ")
            self.handler.printComponents(best_child.components)
            current_node = best_child
            for c in current_node.components:
                componentHolder.append(c)

        return componentHolder
    
    def getUninitializedChildren(self):
        unintializedChildren = []
        print_log("Children: ", logging)
        for key in self.children.keys():
            if self.children[key] == None:
                print_log(str(key)+": None", logging)
                unintializedChildren.append(key)
            else:
                print_log(str(key)+": Expanded", logging)
        return unintializedChildren

    def getComponentsUntilCurrentNode(self):
        componentsHolder = []
        currentNode = self
        while ( currentNode != None ):
            for value in currentNode.components:
                componentsHolder.append(value)
            currentNode = currentNode.parent
        return list(reversed(componentsHolder))    
