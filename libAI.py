import math
import random
import pygame, random, sys, math
import numpy as np
from pygame.locals import *
from BFS import pathfinding


# Select starting node
class AI:

    def getLegalNodes(self, nodes):
        legalNodes = []

        for node in nodes:
            if len(node.relations) < 3:
                legalNodes.append(node)

        return legalNodes

    def getRandom(self, max):
        return random.randint(0, max)

    def getDistance(self, pos1, pos2):
        return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

    def getPathLenght(self, path):
        length = 0
        for i in range(len(path)-1):
            length = length + self.getDistance(path[i-1], path[i])
        return length

    def legitPath(self, path):
        if path[0] == path[-1]:
            if len(path) == 3:
                return False
            else:
                return True
        return True


    def getShortestPath(self, paths):
        shortestPath = None
        shortestLength = None
        for path in paths:
            if self.legitPath(path):
                if shortestLength is None or self.getPathLenght(path) < shortestLength:
                    shortestLength = self.getPathLenght(path)
                    shortestPath = path
        return shortestPath
