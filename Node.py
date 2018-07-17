class Node(object):
    
    operators = ["+", "-"]
    terminals = [1, "x"]

    def __init__(self):
        self.value = None
        self.visits = 0;
        self.reward = 0;
        self.fullyExpanded = False
        self.children = None;

    def iteration(self):
        node = treePolicy()

    def treePolicy(self):
        # selected a node from the tree to expand
        return self

    def rollOut(self):
        # execute rollout and return Reward
        return 0

    def backup(self, node, reward):
        # update all nodes up to the root
        return None

    def expand(self):
        if self.fullyExpanded != True:
            # expand the tree
