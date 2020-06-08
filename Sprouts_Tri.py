import pygame, random, sys, math
import numpy as np
from pygame.locals import *
from scipy.spatial import Delaunay

# TODO
# - Delaunay triangulation

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
        angle = 0
        for i in range(n):
            x = (system.width / 4) * math.cos(angle * 0.0174532925)
            y = (system.width / 4) * math.sin(angle * 0.0174532925)
            addNode((system.width / 2) + x, (system.height / 2) + y)
            angle += 360 / n

    # Method for clearing stored nodes and centroids
    def clearGame(self):
        nodes.clear()
        tempCentroids.clear()


# ------------------------------------------------
# Game controller class
class GameView:

    # Method for updating nodes
    def updateNodes(self):
        for node in nodes:
            if len(node.relations) == 3:
                pygame.draw.circle(system.screen, system.red, (int(node.x), int(node.y)), size)
            else:
                if node.selected:
                    pygame.draw.circle(system.screen, system.blue, (int(node.x), int(node.y)), size)
                else:
                    pygame.draw.circle(system.screen, system.green, (int(node.x), int(node.y)), size)

    # Method for updating nodes
    def updateCentroids(self):
        for centroid in tempCentroids:
            if centroid.selected:
                pygame.draw.circle(system.screen, system.blue, (int(centroid.x), int(centroid.y)), int(size / 2))
            else:
                pygame.draw.circle(system.screen, system.red, (int(centroid.x), int(centroid.y)), int(size / 2))

    # Method
    def updateEdges(self, list):
        for edge in list:

            # Draw path
            i = 0
            for i in range(len(edge)):
                if i + 1 != len(edge):
                    pygame.draw.line(system.screen, system.black, edge[i], edge[i + 1], 5)


# ------------------------------------------------
# Game controller class
class GameLogic:

    def determinant(self, a1, a2, b1, b2):
        return a1*b2 - a2*b1

    def findAngle(self, p1, p2):

        # Find diff
        xdiff = p1[0]-p2[0]
        ydiff = p1[1]-p2[1]

        # Find angle
        angleRadians = math.atan2(xdiff, ydiff)
        angleDegrees = math.degrees(angleRadians)

        return angleDegrees

    def findNewEdge(self, edge):

        p1 = edge[0]
        p2 = edge[1]

        # Find diff
        xdiff = p1[0] - p2[0]
        ydiff = p1[1] - p2[1]

        factor = xdiff/ydiff
        a = factor + 1

        print(self.secondDegreeSolver(a, 0, (20)))

        return a

    def secondDegreeSolver(self, a, b, c):
        d = (b**2) - (4*a*c)
        print(d)

        sol1 = (-b - math.sqrt(d))/(2*a)
        sol2 = (b - math.sqrt(d)) / (2 * a)

        print(sol1, " ", sol2)

    # p1 and p2 is start and end of line 1
    # p3 and p4 is start and end of line 2
    def lineIntersection(self, p1, p2, p3, p4):

        # Find standard form of lines: ax+by+c
        a1 = (p2[1] - p1[1])
        b1 = (p1[0] - p2[0])  # y flipped due to top-left origo
        c1 = (p1[0] * p2[1]) - (p2[0] * p1[1])
        a2 = (p4[1] - p3[1])
        b2 = (p3[0] - p4[0])  # y flipped due to top-left origo
        c2 = (p3[0] * p4[1]) - (p4[0] * p3[1])

        det = self.determinant(a1, a2, b1, b2)
        x = (b2 * c1 - b1 * c2) / det
        y = (a1 * c2 - a2 * c1) / det

        pygame.draw.circle(system.screen, system.blue, (int(x), int(y)), int(size / 2))
        print(x, y)

        if det == 0:
            return False

        if x > system.width:
            return False

        if y > system.height:
            return False

        if x > max(p1[0], p2[0]) or x < min(p1[0], p2[0]):
            return False

        if y > max(p1[1], p2[1]) or y < min(p1[1], p2[1]):
            return False

        return True

    def lineCheck(self, p1, p2):

        if edges is not None:
            for edge in edges:
                for i in range(len(edge)):
                    if i + 1 != len(edge):
                        if self.lineIntersection(p1, p2, edge[i], edge[i+1]):
                            print("line error at: ", p1, p2, edge[i], edge[i+1])
                            return False

        return True


# ------------------------------------------------
# Method for adding vertices
def addNode(x, y):
    v = Node(len(nodes), x, y, [], False, False)
    nodes.append(v)


def addCentroid(a, b, c):
    o_x = (a[0] + b[0] + c[0])/3
    o_y = (a[1] + b[1] + c[1])/3
    p = Centroid(len(tempCentroids), o_x, o_y, [a,b,c], False)
    tempCentroids.append(p)


def nodeCollision(node, mousePos):
    if not ((abs(mousePos[0] - node.x)) < margin) & ((abs(mousePos[1] - node.y)) < margin):
        return False
    return True


def getNodeArray():
    nodesTemp = []

    # Get nodes
    for node in nodes:
        nodesTemp.append([node.x, node.y])

    # Get existing centroids
    for cen in centroids:
        nodesTemp.append([cen.x, cen.y])

    nodesTemp.append([0, 0])
    nodesTemp.append([0, system.height])
    nodesTemp.append([system.width, 0])
    nodesTemp.append([system.width, system.height])

    nodesTemp = np.array(nodesTemp)
    return nodesTemp


def drawDelaunay():
    points = getNodeArray()
    tri = Delaunay(points)

    for slice in tri.simplices:
        abc = [points[slice[0]], points[slice[1]], points[slice[2]]]

        pygame.draw.line(system.screen, system.red, abc[0], abc[1], 5)
        pygame.draw.line(system.screen, system.red, abc[1], abc[2], 5)
        pygame.draw.line(system.screen, system.red, abc[2], abc[0], 5)

        addCentroid(abc[0], abc[1], abc[2])


def nearCentroids(node1):
    points = getNodeArray()
    tri = Delaunay(points)

    for slice in tri.simplices:
        if nodes.index(node1) in slice:
            abc = [points[slice[0]], points[slice[1]], points[slice[2]]]

            pygame.draw.line(system.screen, system.red, abc[0], abc[1], 5)
            pygame.draw.line(system.screen, system.red, abc[1], abc[2], 5)
            pygame.draw.line(system.screen, system.red, abc[2], abc[0], 5)

            addCentroid(abc[0], abc[1], abc[2])


# DOESNT WORK BECAUSE OF START REGISTER
def isCenValidTarget(pos1, pos2):

    if len(edges) > 0:
        edgesTemp = edges.copy()
        tempPath2 = tempPath.copy()
        edgesTemp.append(tempPath2)

        for edge in edgesTemp:
            for i in range(len(edge)):
                if i + 1 != len(edge):
                    print(edge[i])
    return True


def cleanScreen():
    system.screen.fill(system.white)

# ------------------------------------------------
# Initialize classes
view = GameView()
controller = GameController()
system = System()
logic = GameLogic()

# Node related variables
nodes = []
size = 20
margin = size

# Edge related variables
tempPath = []
edges = []

# Centroid related variables
tempCentroids = []
centroids = []
activeNode = None

# Initialize game
system.init()
controller.startGame(6)

# addCentroid(nodes[0], nodes[1], nodes[2])

# Game loop -----------------------------
while 1:
    for event in pygame.event.get():
        mousePos = pygame.mouse.get_pos()
        # Quit game
        if event.type == QUIT:
            sys.exit()

        # TESTING START --------------------------------
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            if event.key == K_a:
                drawDelaunay()
            if event.key == K_b:
                view.updateCentroids()
            if event.key == K_SPACE:
                centroidsTempTemp = tempCentroids.copy()
                centroidsTemp = centroids.copy()
                tempCentroids.clear()
                centroids.clear()
                system.screen.fill(system.white)
                centroids = centroidsTemp.copy()

            if event.key == K_1:
                GameController.startGame(None, 1)
            if event.key == K_2:
                GameController.startGame(None, 2)
            if event.key == K_3:
                GameController.startGame(None, 3)
            if event.key == K_4:
                GameController.startGame(None, 4)
            if event.key == K_5:
                GameController.startGame(None, 5)
            if event.key == K_6:
                GameController.startGame(None, 6)
            if event.key == K_7:
                GameController.startGame(None, 7)
            if event.key == K_8:
                GameController.startGame(None, 8)
            if event.key == K_9:
                GameController.startGame(None, 9)
        # TESTING END --------------------------------
        # Select node
        elif event.type == MOUSEBUTTONDOWN:

            for node in nodes:
                if nodeCollision(node, mousePos):

                    # If node is selected - SELECT NEW NODE || CONNECT TO CENTROID
                    if activeNode is not None:
                        if activeNode is not node:  # CHANGE THIS TO CHECK THAT NODE IS ALLOWED TO SELF-CONNECT
                            if len(node.relations) < 3:

                                # Check for line intersection

                                # posNode = [node.x, node.y]
                                # posCen = [centroids[-1].x, centroids[-1].y]
                                # if logic.lineCheck(posCen, posNode): VIRKER IKKE

                                # Finalize path
                                tempPath.append([node.x, node.y])
                                path = tempPath.copy()
                                edges.append(path)

                                # Add node
                                nodePlace = None
                                if len(tempPath) > 2:
                                    nodePlace = tempPath[int(len(tempPath)/2)]
                                else:
                                    nodePlace = [int((activeNode.x+node.x)/2), int((activeNode.y+node.y)/2)]
                                addNode(nodePlace[0], nodePlace[1])

                                # Append relations
                                nodes.__getitem__(activeNode.id).relations.append(nodes[-1].id)
                                nodes.__getitem__(node.id).relations.append(nodes[-1].id)
                                nodes.__getitem__(-1).relations.append(activeNode.id)
                                nodes.__getitem__(-1).relations.append(node.id)
                                nodes.__getitem__(activeNode.id).selected = False

                                # Reset
                                activeNode = None
                                tempCentroids.clear()
                                tempPath.clear()

                    # If no node is selected - SELECT NODE
                    else:
                        if len(node.relations) < 3:
                            # Activate new node
                            activeNode = node
                            tempPath.append([node.x, node.y])
                            print("node ", node.id, " selected.")

                            # Mark selected
                            node.selected = True

            # Select centroid
            if activeNode is not None:
                for cen in tempCentroids:
                    if nodeCollision(cen, mousePos):
                        # if isCenValidTarget([int(activeNode.x), int(activeNode.y)], [int(cen.x), int(cen.y)]):
                        cen.selected = True
                        centroids.append(cen)
                        print("cen ", cen.id, " selected.")
                        if [cen.x, cen.y] not in tempPath:
                            tempPath.append([cen.x, cen.y])

            # Update delauney on click
            cleanScreen()
            tempCentroids.clear()
            drawDelaunay()
            view.updateEdges([tempPath])

    # Update every iteration
    view.updateEdges(edges)
    view.updateNodes()
    view.updateCentroids()

    pygame.display.update()
