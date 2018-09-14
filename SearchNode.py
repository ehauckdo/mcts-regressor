from SolutionHandler import SolutionHandler
import random

class SearchNode(object):

    def __init__(self, handler=SolutionHandler(), parent=None):
        random.seed(0)
        self.value = []
        self.parent = parent
        self.handler = handler    
 
    def iteration(self):
        node = self.treePolicy()
        part_sol = node.rollOut()
        node.backup(part_sol.getReward())

    def treePolicy(self):
        return SearchNode()

    def uct(self):
        return SearchNode()

    def expand(self):
        return SearhNode()

    def rollOut(self):
        return SolutionHandler()

    def backup(self, reward):
        return 
