import copy
import sys
import random
import math
import logging
import numpy as np
from Utility.Utility import normalize
from SolutionHandler import SolutionHandler

printlog = True

class SearchNode(object):

    def __init__(self, handler=SolutionHandler(), parent=None, components=[]):
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
        self.children = {}  
        valueHolder = self.getComponentsUntilCurrentNode()
        
        logging.debug("Initializing children list... Expression up to now:")
        logging.debug(self.handler.printComponents(valueHolder))
        
        possible_children = self.handler.getPossibleChildren(valueHolder)
        if len(possible_children) == 0:
            self.fullyExpanded = True
            logging.debug("This node can not have children.")
        for component in possible_children:
            self.children[component] = None
        logging.debug("Available children: (len: "+str(len(possible_children))+" ")
        logging.debug(self.handler.printComponents(possible_children))

    def iteration(self):
        logging.info("======== New Iteration =========")
        self.handler.partialSolution = copy.deepcopy(self.components)
        node = self.treePolicy()
        reward = node.rollOut()
        node.backup(reward)

    def treePolicy(self):
        logging.info("Executing Tree Policy...")
        selectedNode = self
         
        while selectedNode.children:
            if selectedNode.fullyExpanded is False:
                logging.info("Expanding node:"+"\n".join(self.handler.printComponents(selectedNode.components)))
                logging.info("Number of uninitialized children: "+str(len(selectedNode.getUninitializedChildren())))
                expandedNode = selectedNode.expand()
                if len(selectedNode.getUninitializedChildren()) == 0:
                    logging.info("This node is now fully expanded.")
                    selectedNode.fullyExpanded = True
                selectedNode = expandedNode
                break
            else:
                selectedNode = selectedNode.uct()
        logging.info("Selected node from treePolicy: "+"\n".join(self.handler.printComponents()))
        return selectedNode

    def uct(self):
        logging.info("Calculating UCT from node depth "+str(self.depth))
        selected_node = self
        selected_node_value = None
        best_value = -sys.maxint

        for key in self.children.keys():
            child_node = self.children[key]
        
            total_reward = child_node.reward
            child_value = total_reward / child_node.visits

            child_value = normalize(child_value, self.bounds[0], self.bounds[1])

            uct_value = child_value + self.C * math.sqrt(math.log(self.visits) / child_node.visits)
            
            logging.debug("Checking child: "+str(key))
            logging.debug("Bounds: "+str(self.bounds[0])+", "+str(self.bounds[1]))
            logging.debug("UCT value: "+str(uct_value))

            if uct_value > best_value:
                selected_node = child_node
                selected_node_value = key
                best_value = uct_value
        
        if selected_node == None:
            raise ValueError('No node was selected in UCT')

        self.handler.partialSolution.append(selected_node_value)
        #logging.info("Selected node by UCT: "+self.handler.printComponents(selected_node.components))
        logging.info("Selected node by UCT: \n"+"\n".join(self.handler.printComponents(selected_node.components)))
        return selected_node

    def expand(self):
        uninitializedChildren = self.getUninitializedChildren()

        selectedComponent = random.choice(uninitializedChildren)
        self.handler.partialSolution.append(selectedComponent)
        newChild = SearchNode(self.handler, self, [selectedComponent])
        self.children[selectedComponent] = newChild
        
        logging.info("Expanded child: "+"\n".join(self.handler.printComponents(newChild.components)))
        return newChild

    def rollOut(self):
        logging.info("Executing rollout...")
        current_depth = self.depth
        componentHolder = copy.deepcopy(self.handler.partialSolution)
        
        while self.handler.expandSolution(componentHolder) == True:
            current_depth += 1 

        logging.info("Rollouted expression: \n"+"\n".join(self.handler.printComponents(componentHolder)))
        reward = self.handler.getRolloutReward(componentHolder)
        reward = sys.maxint if np.isinf(reward) else reward
        reward = -sys.maxint if np.isneginf(reward) else reward
        logging.info("Rollout completed. Reward: "+str(reward))

        return reward

    def backup(self, reward):
        node = self
        logging.info("Backing up reward...")
        while node != None:
            if reward < node.bounds[0]:
                node.bounds[0] = reward
            if reward > node.bounds[1]:
                node.bounds[1] = reward
            node.visits += 1
            node.reward += reward
            logging.debug("Updated bounds in node depth "+str(node.depth)+": "+str(node.bounds[0])+", "+str(node.bounds[1]))
            node = node.parent

    def bestChild(self):
        logging.info("Searching for best child from Root...")
        best_child = None
        most_visits = -1
        for key in self.children.keys():
            logging.info("Checking key "+str(key))
            logging.info("visits: "+str(self.children[key].visits)+", reward: "+str(self.children[key].reward))
            if self.children[key] == None:
                continue
            if self.children[key].visits > most_visits:
                best_child = self.children[key]
                most_visits = self.children[key].visits
        return best_child

    def bestBranch(self):
        logging.info("Searching for best branch from Root...")
        componentHolder = copy.deepcopy(self.components)
        current_node = self
        while len(current_node.children.keys()) != 0:
            print("Checking node depth "+str(current_node.depth))
            most_visits = -1
            for key in current_node.children.keys():
                logging.info("Checking key "+str(key))
                logging.info("visits: "+str(current_node.children[key].visits)+", reward: "+str(current_node.children[key].reward))
                if current_node.children[key] == None:
                    continue
                if current_node.children[key].visits > most_visits:
                    best_child = current_node.children[key]
                    most_visits = current_node.children[key].visits
            logging.info("Selected node: ")
            logging.info("\n".join(self.handler.printComponents(best_child.components)))
            current_node = best_child
            for c in current_node.components:
                componentHolder.append(c)
        logging.info("Best branch: \n"+"\n".join(self.handler.printComponents(componentHolder)))
        return componentHolder
    
    def getUninitializedChildren(self):
        unintializedChildren = []
        logging.debug("Verifying uninitialized children: ")
        for key in self.children.keys():
            if self.children[key] == None:
                logging.debug(str(key)+": None")
                unintializedChildren.append(key)
            else:
                logging.debug(str(key)+": Expanded")
        return unintializedChildren

    def getComponentsUntilCurrentNode(self):
        componentsHolder = []
        currentNode = self
        while ( currentNode != None ):
            for value in currentNode.components:
                componentsHolder.append(value)
            currentNode = currentNode.parent
        return list(reversed(componentsHolder))    
