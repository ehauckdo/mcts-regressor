import logging
import StringIO
import time
from SearchNode import SearchNode
from SolutionHandler import SolutionHandler

class MCTS(object):

    def __init__(self, handler=SolutionHandler(), iterations=50000):
        self.iterations = iterations
        self.handler = handler
        self.root = SearchNode(handler)

    def run(self):
        for i in range(self.iterations):
            self.root.iteration()
