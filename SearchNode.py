from PartialSolution import PartialSolution

class SearchNode(object):

    def __init__(self, parent=None, part_sol=PartialSolution()):
        self.parent = parent
        self.value = part_sol
        self.objective = None if parent == None else parent.objective
        
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
        return PartialSolution()

    def backup(self, reward):
        return 
