import pygame, random, sys, math
from pygame.locals import *
from Triangulation import Triangulation
from libSystem import *
from libNode import *
from libController import *


# ------------------------------------------------
# Triangulation logic
class TriangulationLogic:

    dt = Triangulation()

    # Triangulation related variables
    centroids = []
    chosenCenter = []
    neighbours = []
    centersize = 8

    def initializeTriangulation(self, nodes):
        # Insert nodes
        for n in nodes:
            self.dt.addPoint([n.x, n.y])

        # Add corners
        self.dt.addCornerNodes()
        self.centroids = self.dt.exportInCenters()

    def getCentroids(self):
        return self.centroids

    def getCentersize(self):
        return self.centersize

    def updateCentroids(self):
        self.centroids = self.dt.exportInCenters()

    def clearNeighbours(self):
        self.neighbours.clear()

    def clearChosenCenter(self):
        self.chosenCenter.clear()

    def resetGame(self):
        self.centroids.clear()
        self.chosenCenter.clear()
        self.neighbours.clear()
        self.dt.resetTriangulation()
