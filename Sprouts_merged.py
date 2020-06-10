import pygame, random, sys, math
import numpy as np
from pygame.locals import *
from scipy.spatial import Delaunay
from Triangulation import Triangulation
from BFS import pathfinding

# TODO
# - Nodes NOT connecting to center, but to mousepos in node instead

# ------------------------------------------------
# Node class for initializing and operating on vertices
class System:

    # System related variables
    width = 800
    height = 800

    # Color definitions
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0
    green = 0, 255, 0
    blue = 0, 0, 255
    gray = 150, 150, 150

    # Screen
    screen = pygame.display.set_mode((width, height), RESIZABLE)
    background = pygame.Surface(screen.get_size())

    def init(self):
        pygame.init()
        pygame.display.set_caption("Sprouts")
        self.background.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        random.seed()


# ------------------------------------------------
# Node class for initializing and operating on vertices
class Node:
    def __init__(self, id, x, y, relations, locked, selected):
        self.id = id
        self.x = x
        self.y = y
        self.relations = relations
        self.locked = locked
        self.selected = selected


# ------------------------------------------------
# Centroid class
class Centroid:
    def __init__(self, id, x, y, points, selected):
        self.id = id
        self.x = x
        self.y = y
        self.points = points
        self.selected = selected


# ------------------------------------------------
# Game controller class
class GameController:

    # Method for setting up initial nodes
    def startGame(self, n):
        nodes.clear()
        angle = 0
        for i in range(n):
            x = (system.width / 3.5) * math.cos(angle * 0.0174532925)
            y = (system.width / 3.5) * math.sin(angle * 0.0174532925)
            addNode((system.width / 2) + x, (system.height / 2) + y)
            angle += 360 / n

    # Method for clearing stored nodes and centroids
    def clearGame(self):
        nodes.clear()
        #tempCentroids.clear()


# ------------------------------------------------
# Game controller class
class TriangulationLogic:

    dt = Triangulation()

    # Triangulation related variables
    centroids = []
    chosenCenter = []
    neighbours = []

    def initializeTriangulation(self):
        # Insert nodes
        for n in nodes:
            self.dt.addPoint([n.x, n.y])

        # Add corners
        self.dt.addCornerNodes()
        self.centroids = self.dt.exportInCenters()

    def updateCentroids(self):
        self.centroids = self.dt.exportInCenters()

    def clearNeighbours(self):
        self.neighbours.clear()

    def clearChosenCenter(self):
        self.chosenCenter.clear()


# ------------------------------------------------
# Game view class
class GameView:

    # Method for updating nodes
    def updateNodes(self):
        for node in nodes:
            if len(node.relations) == 3:
                pygame.draw.circle(system.screen, system.green, (int(node.x), int(node.y)), size)
            else:
                pygame.draw.circle(system.screen, system.black, (int(node.x), int(node.y)), size)

    # Method for updating edges
    def updateEdges(self):
        #  for edge in edges:
        for [sPos, ePos] in edges:
            pygame.draw.line(system.screen, system.red, sPos, ePos, 5)

    # Method for updating delaunay nodes
    def updateCentroids(self):
        for [x, y] in triLogic.centroids:
            pygame.draw.circle(system.screen, system.blue, (int(x), int(y)), centersize)

    def updateTriLines(self):
        for dEdge in triLogic.dt.allEdges:
            pygame.draw.line(system.screen, system.gray, dEdge.start.coordinates, dEdge.end.coordinates, 5)

    def updateNeighbours(self):
        for [x, y] in triLogic.neighbours:
            pygame.draw.circle(system.screen, system.red, (int(x), int(y)), centersize)

    # Method updating screen
    def updateScreen(self):
        system.screen.fill(system.white)
        view.updateTriLines()
        view.updateEdges()
        view.updateCentroids()
        view.updateNeighbours()
        view.updateNodes()


# ------------------------------------------------
# Method for adding vertices
def addNode(x, y):
    v = Node(len(nodes), x, y, [], False, False)
    nodes.append(v)


# Method for appending position to line
def appendPos(line, pos):
    line.append(pos)


# Method for checking whether a node
def nodeCollision(node, mousePos, type):
    color = system.screen.get_at(pygame.mouse.get_pos())
    if color == system.black and moved:
        return False
    if type == "node":
        if not ((abs(mousePos[0] - node.x)) < margin) & ((abs(mousePos[1] - node.y)) < margin):
            return False
        return True
    else:
        if not ((abs(mousePos[0] - node[0])) < margin) & ((abs(mousePos[1] - node[1])) < margin):
            return False
        return True


# Method for checking a position has reached a certain distance away from a node
def reverseNodeCollision(node, mousePos):
    if not ((abs(mousePos[0] - node.x)) > size) & ((abs(mousePos[1] - node.y)) > size):
        return False
    return True


# Method for removing placeholder item
def removePlaceholder():
    if activeItem is not None:
        if -1 in nodes.__getitem__(activeItem).relations:
            nodes.__getitem__(activeItem).relations.remove(-1)


# ------------------------------------------------
# Initialize classes
view = GameView()
system = System()
controller = GameController()
triLogic = TriangulationLogic()

# Node related variables
nodes = []
size = 10
margin = size

# Edge related variables
edges = []

# Drawing related variables
activeNode = None
activeItem = None
moved = False
activePos = None

# Triangulation related variables
centersize = 8

# Initialize game
system.init()
controller.startGame(4)
triLogic.initializeTriangulation()

# TEST VARIABLES
space = False

# Game loop -----------------------------
while 1:
    for event in pygame.event.get():
        mousePos = pygame.mouse.get_pos()

        # Quit game
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_SPACE:
                space = True
                system.screen.fill(system.white)
            if event.key == K_BACKSPACE:
                space = False

        # Mouse action -----------------------------
        elif event.type == MOUSEBUTTONDOWN:

            # No active node ------------------------
            if activePos is None:
                for node in nodes:
                    if nodeCollision(node, mousePos, "node"):
                        if len(node.relations) < 3:
                            activeNode = node
                            activeItem = node.id
                            activePos = [activeNode.x, activeNode.y]
                            node.relations.append(-1)
                            triLogic.neighbours = triLogic.dt.exportNeighbours([node.x, node.y], "node", triLogic.chosenCenter, [activeNode.x, activeNode.y])

            # Active node ---------------------------
            if activePos is not None:

                # Select centroid -------------------
                for centerNode in triLogic.centroids:
                    if centerNode in triLogic.neighbours:
                        if nodeCollision(centerNode, mousePos, "centerNode"):
                            edges.append([activePos, centerNode])
                            activePos = centerNode
                            triLogic.chosenCenter.append(centerNode)

                            triLogic.neighbours.clear()
                            triLogic.neighbours = triLogic.dt.exportNeighbours(centerNode,
                                    "centerNode", triLogic.chosenCenter, [activeNode.x, activeNode.y])

                # Select end node ------------------
                for node in nodes:
                    if nodeCollision(node, mousePos, "node"):
                        if [node.x, node.y] in triLogic.neighbours:
                            if len(node.relations) < 3:
                                edges.append([activePos, [node.x, node.y]])
                                """
                                paths = pathfinding(TriangulationLogic.dt, [activeNode.x, activeNode.y], [node.x, node.y]).paths
                                for path in paths:
                                    print(path)
                                    for i, p in enumerate(path):
                                        if not i == 0:
                                            edges.append([path[i-1], p])
                                print(len(paths))
                                """

                                if len(triLogic.chosenCenter) > 0:
                                    mid = triLogic.chosenCenter[int(len(triLogic.chosenCenter) / 2)]
                                else:
                                    mid = [(activePos[0] + mousePos[0]) / 2, (activePos[1] + mousePos[1]) / 2]
                                addNode(mid[0], mid[1])

                                # Remove placeholder relation
                                nodes.__getitem__(activeItem).relations.remove(-1)

                                # Add relations between connected nodes
                                nodes.__getitem__(activeItem).relations.append(nodes[-1].id)
                                nodes.__getitem__(node.id).relations.append(nodes[-1].id)
                                nodes.__getitem__(-1).relations.append(activeItem)
                                nodes.__getitem__(-1).relations.append(node.id)

                                # Add new path and node
                                triLogic.dt.addPath([activeNode.x, activeNode.y], [node.x, node.y], triLogic.chosenCenter, mid)
                                triLogic.updateCentroids()
                                triLogic.clearChosenCenter()
                                triLogic.clearNeighbours()

                                activeNode = None
                                activePos = None
                                activeItem = None

                            # Remove placeholder relation
                            removePlaceholder()

                            # win detection
                            unlockedNodes = []
                            Check = True
                            morePaths = False
                            for n in nodes:
                                #If there are a node with more than one liberty it is sure that the game is not done
                                if len(n.relations) < 2:
                                    Check = False
                                    break
                                elif len(n.relations) < 3:
                                    unlockedNodes.append(n)
                            if Check:
                                #Use of BFS to check if there are paths between unlocked nodes
                                for i, uNode in enumerate(unlockedNodes):
                                    for u2Node in unlockedNodes[i+1:]:
                                        paths = pathfinding(TriangulationLogic.dt,
                                                            [uNode.x, uNode.y],
                                                            [u2Node.x, u2Node.y]).paths
                                        if len(paths) > 0:
                                            morePaths = True
                                            break
                                    if morePaths:
                                        break
                                    #If morePaths = False and we have searched all connections then the game is done
                                    elif i == len(unlockedNodes) - 1:
                                        print("the game is done")

    view.updateScreen()

    # Update every iteration
    if space is True:
        system.screen.fill(system.white)
        view.updateNodes()
        view.updateEdges()

    pygame.display.update()
