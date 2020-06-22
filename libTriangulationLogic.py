import pygame, random, sys, math
from pygame.locals import *
from Triangulation import Triangulation


# ------------------------------------------------
# Triangulation logic
class TriangulationLogic:
    def __init__(self):
        self.dt = Triangulation()
        # Triangulation related variables
        self.centroids = []
        self.chosenCenter = []
        self.neighbours = []
        self.centersize = 8

#    def getDt(self):
#        return self.dt

    def getCentroids(self):
        return self.centroids

    def setCentroids(self, centroids):
        self.centroids = centroids

    def getChosenCenter(self):
        return self.chosenCenter

    def getNeighbours(self):
        return self.neighbours

    def setNeighbours(self, neighbours):
        self.neighbours = neighbours

    def getCentersize(self):
        return self.centersize

    def setCentersize(self, size):
        self.centersize = size

    def initializeTriangulation(self, nodes):
        # Insert nodes
        for n in nodes:
            self.dt.addPoint(n.getPos())

        # Add corners
        self.dt.addCornerNodes()
        self.setCentroids(self.dt.exportInCenters())

    def updateCentroids(self):
        self.setCentroids(self.dt.exportInCenters())

    def clearNeighbours(self):
        self.getNeighbours().clear()

    def clearChosenCenter(self):
        self.getChosenCenter().clear()
