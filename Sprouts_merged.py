import pygame, random, sys, math
import numpy as np
from pygame.locals import *
from Triangulation import Triangulation
#from graphSearch import *
from BFS import pathfinding
import time


# -------------------- ----------------------------
# System class
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
        self.pos = [self.x, self.y]


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

    # Node related variables
    nodes = []
    size = 10
    edges = []
    currentEdges = []

    # Drawing related variables
    activeNode = None
    activeItem = None
    activePos = None

    #
    done = False
    error = False
    turn = 0

    # Method for adding vertices
    def addNode(self, x, y):
        v = Node(len(self.nodes), x, y, [], False, False)
        self.nodes.append(v)

    def findNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    def getNodes(self):
        return self.nodes

    def getEdges(self):
        return self.edges

    def setActiveNode(self, node):
        self.activeNode = node

    def getActiveNode(self):
        return self.activeNode

    def setActiveItem(self, item):
        self.activeItem = item

    def getActiveItem(self):
        return self.activeItem

    def setActivePos(self, pos):
        self.activePos = pos

    def getActivePos(self):
        return self.activePos

    def getPlayer(self):
        return self.turn % 2 + 1

    def getTurn(self):
        return self.turn

    def setTurn(self, turn):
        print(self.turn)
        self.turn = turn

    def resetGame(self):
        self.nodes.clear()
        self.edges.clear()
        self.currentEdges.clear()
        self.activePos = None
        self.activeItem = None
        self.activeNode = None
        self.error = False
        self.done = False
        self.turn = 0

    # Method for setting up initial nodes
    def startGame(self, n):
        self.nodes.clear()
        angle = 0
        for i in range(n):
            x = (system.width / 3.5) * math.cos(angle * 0.0174532925)
            y = (system.width / 3.5) * math.sin(angle * 0.0174532925)
            self.addNode((system.width / 2) + x, (system.height / 2) + y)
            angle += 360 / n

    # Method for checking whether a node
    def nodeCollision(self, node, mousePos, type):
        if type == "node":
            if not ((abs(mousePos[0] - node.x)) < self.size) & ((abs(mousePos[1] - node.y)) < self.size):
                return False
            return True
        else:
            if not ((abs(mousePos[0] - node[0])) < self.size) & ((abs(mousePos[1] - node[1])) < self.size):
                return False
            return True

    # Method for removing placeholder item
    def removePlaceholder(self):
        if self.getActiveItem() is not None:
            if -1 in self.getNodes().__getitem__(self.getActiveItem()).relations:
                self.nodes.__getitem__(self.getActiveItem()).relations.remove(-1)


# ------------------------------------------------
# Game controller class
class TriangulationLogic:

    dt = Triangulation()

    # Triangulation related variables
    centroids = []
    chosenCenter = []
    neighbours = []
    centersize = 8

    def initializeTriangulation(self):
        # Insert nodes
        for n in controller.getNodes():
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


# ------------------------------------------------
# Game view class
class GameView:

    font = pygame.font.SysFont(None, 40)
    back_button = pygame.Rect(20, 20, 100, 50)
    restart_button = pygame.Rect(140, 20, 100, 50)

    # Method for updating nodes
    def updateNodes(self):
        for node in controller.getNodes():
            if len(node.relations) == 3:
                pygame.draw.circle(system.screen, system.green, (int(node.x), int(node.y)), controller.size)
            else:
                pygame.draw.circle(system.screen, system.black, (int(node.x), int(node.y)), controller.size)

    # Method for updating edges
    def updateEdges(self):
        #  for edge in edges:
        for [sPos, ePos] in controller.getEdges():
            pygame.draw.line(system.screen, system.red, sPos, ePos, 5)

    # Method for updating delaunay nodes
    def updateCentroids(self):
        for [x, y] in triLogic.centroids:
            pygame.draw.circle(system.screen, system.blue, (int(x), int(y)), triLogic.getCentersize())

    def updateTriLines(self):
        for dEdge in triLogic.dt.allEdges:
            pygame.draw.line(system.screen, system.gray, dEdge.start.coordinates, dEdge.end.coordinates, 5)

    def updateNeighbours(self):
        for [x, y] in triLogic.neighbours:
            pygame.draw.circle(system.screen, system.red, (int(x), int(y)), triLogic.getCentersize())

    def updateGraphEdges(self, graphEdges):
        if len(graphEdges) != 0:
            for edge in graphEdges:
                print(edge[0].pos, edge[1].pos)
                # pygame.draw.line(system.screen, system.green, edge[0].pos, edge[1].pos, 5)

    def updatePath(self, path):
        if len(path) != 0:
            for i in range(len(path)):
                if i+1 < len(path):
                    pygame.draw.line(system.screen, system.blue, path[i], path[i+1], 5)

    def displayPlayer(self):
        if controller.getPlayer() == 1:
            self.drawText('Player 1', self.font, system.blue, system.screen, system.height/2, system.width/20)
        elif controller.getPlayer() == 2:
            self.drawText('Player 2', self.font, system.red, system.screen, system.height/2, system.width/20)

    def displayWinner(self):
        if controller.getPlayer() == 1:
            return view.drawPopUp('Player 2 wins!'.format())
        elif controller.getPlayer() == 2:
            return view.drawPopUp('Player 1 wins!'.format())

    # Method updating screen
    def updateScreen(self):
        system.screen.fill(system.white)
        view.drawGUI()
        view.updateTriLines()
        view.updateEdges()
        view.updateCentroids()
        view.updateNeighbours()
        view.updateNodes()
        view.displayPlayer()

    # Method for drawing text on the screen
    def drawText(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def drawGUI(self):
        pygame.draw.rect(system.screen, system.black, view.back_button)
        view.drawText('back', self.font, system.white, system.screen, 70, 45)
        pygame.draw.rect(system.screen, system.black, view.restart_button)
        view.drawText('restart', self.font, system.white, system.screen, 190, 45)

    def drawPopUp(self, text):
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pupup_frame = pygame.Rect(195, 295, 410, 210)
        popup = pygame.Rect(200, 300, 400, 200)
        popup_button = pygame.Rect(350, 425, 100, 50)
        pygame.draw.rect(system.screen, (0,0,0), pupup_frame)
        pygame.draw.rect(system.screen, (255,255,255), popup)
        if popup_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(system.screen, (0,150,0), popup_button)
            if click:
                return True
        else:
            pygame.draw.rect(system.screen, (0,0,0), popup_button)
        view.drawText(text, view.font, (0,0,0), system.screen, 400, 350)
        view.drawText('Close', view.font, (255,255,255), system.screen, 400, 450)


# -------------------------------------------------------------------
# --------------------------- MAIN GAME -----------------------------
# -------------------------------------------------------------------
def playGame(amount, txt, txt_input):
    controller.resetGame()
    triLogic.resetGame()
    # Initialize game
    system.init()
    controller.startGame(amount)
    triLogic.initializeTriangulation()

    if txt:
        for inp in txt_input:
            s = controller.findNode(int(inp[0])-1)
            e = controller.findNode(int(inp[2])-1)

            if len(s.relations) < 3 and len(e.relations) < 3:
                paths = pathfinding(TriangulationLogic.dt, [s.x, s.y], [e.x, e.y]).paths

                if len(paths) > 0:
                    print("more moves")
                    i = random.randint(0, len(paths)-1)

                    for j, point in enumerate(paths[i]):
                        if not j == 0:
                            controller.edges.append([paths[i][j-1], point])
                            if not point == paths[i][-1]:
                                triLogic.chosenCenter.append(point)

                    if len(triLogic.chosenCenter) > 0:
                        mid = triLogic.chosenCenter[int(len(triLogic.chosenCenter) / 2)]
                    else:
                        mid = [(s.x + e.x) / 2,
                               (s.y + e.y) / 2]
                    controller.addNode(mid[0], mid[1])

                    # Add relations between connected nodes
                    s.relations.append(e.id)
                    e.relations.append(s.id)

                    # Add new path and node
                    triLogic.dt.addPath([s.x, s.y], [e.x, e.y], triLogic.chosenCenter, mid)
                    triLogic.updateCentroids()
                    triLogic.clearChosenCenter()

                    controller.setTurn(controller.getTurn()+1)

                    view.updateScreen()
                    pygame.display.update()

                else:
                    controller.error = True
                    break

            time.sleep(2.0)

        while controller.error:
            view.updateScreen()
            close = view.drawPopUp('Unable to make the move.')
            pygame.display.update()
            if close:
                return 0

        while 1:
            view.updateScreen()
            close = view.drawPopUp('No more moves in file.')
            pygame.display.update()
            if close:
                return 0

    else:
        # Game loop -----------------------------
        while 1:
            if controller.done:
                view.updateScreen()
                close = view.displayWinner()
                pygame.display.update()
                if close:
                    return 0
            else:
                for event in pygame.event.get():
                    mousePos = pygame.mouse.get_pos()

                    # Quit game
                    if event.type == QUIT:
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return 0
                        elif event.key == K_BACKSPACE:
                            return 1

                    # Mouse action ------------------------------
                    elif event.type == MOUSEBUTTONDOWN:
                        # Check if the buttons are pressed ------
                        if view.back_button.collidepoint(pygame.mouse.get_pos()):
                            return 0
                        elif view.restart_button.collidepoint(pygame.mouse.get_pos()):
                            return 1

                        # No active node ------------------------
                        if controller.getActivePos() is None:
                            for node in controller.getNodes():
                                if controller.nodeCollision(node, mousePos, "node"):
                                    if len(node.relations) < 3:
                                        controller.setActiveNode(node)
                                        controller.setActiveItem(node.id)
                                        controller.setActivePos([controller.getActiveNode().x, controller.getActiveNode().y])
                                        node.relations.append(-1)
                                        triLogic.neighbours = triLogic.dt.exportNeighbours([node.x, node.y], "node", triLogic.chosenCenter, [controller.getActiveNode().x, controller.getActiveNode().y])

                        # Active node ---------------------------
                        if controller.getActivePos() is not None:

                            # Select centroid -------------------
                            for centerNode in triLogic.centroids:
                                if centerNode in triLogic.neighbours:
                                    if controller.nodeCollision(centerNode, mousePos, "centerNode"):

                                        triLogic.neighbours.clear()
                                        triLogic.neighbours = triLogic.dt.exportNeighbours(centerNode,
                                                "centerNode", triLogic.chosenCenter, [controller.getActiveNode().x, controller.getActiveNode().y])

                                        if len(triLogic.neighbours) > 0:
                                            controller.edges.append([controller.getActivePos(), centerNode])
                                            controller.currentEdges.append([controller.getActivePos(), centerNode])
                                            controller.setActivePos(centerNode)
                                            triLogic.chosenCenter.append(centerNode)
                                        else:
                                            for edge in controller.currentEdges:
                                                controller.edges.remove(edge)
                                            controller.nodes.__getitem__(controller.getActiveItem()).relations.remove(
                                                -1)
                                            triLogic.updateCentroids()
                                            triLogic.clearChosenCenter()
                                            triLogic.clearNeighbours()
                                            controller.currentEdges.clear()
                                            controller.setActiveNode(None)
                                            controller.setActivePos(None)
                                            controller.setActiveItem(None)

                            # Select end node ------------------
                            for node in controller.getNodes():
                                if controller.nodeCollision(node, mousePos, "node"):
                                    if [node.x, node.y] in triLogic.neighbours:
                                        if len(node.relations) < 3:
                                            controller.edges.append([controller.getActivePos(), [node.x, node.y]])

                                            if len(triLogic.chosenCenter) > 0:
                                                mid = triLogic.chosenCenter[int(len(triLogic.chosenCenter) / 2)]
                                            else:
                                                mid = [(controller.getActivePos()[0] + mousePos[0]) / 2, (controller.getActivePos()[1] + mousePos[1]) / 2]
                                            controller.addNode(mid[0], mid[1])

                                            # Remove placeholder relation
                                            controller.nodes.__getitem__(controller.getActiveItem()).relations.remove(-1)

                                            # Add relations between connected nodes
                                            controller.nodes.__getitem__(controller.getActiveItem()).relations.append(controller.nodes[-1].id)
                                            controller.nodes.__getitem__(node.id).relations.append(controller.nodes[-1].id)
                                            controller.nodes.__getitem__(-1).relations.append(controller.getActiveItem())
                                            controller.nodes.__getitem__(-1).relations.append(node.id)

                                            # Add new path and node
                                            triLogic.dt.addPath([controller.getActiveNode().x, controller.getActiveNode().y], [node.x, node.y], triLogic.chosenCenter, mid)
                                            triLogic.updateCentroids()
                                            triLogic.clearChosenCenter()
                                            triLogic.clearNeighbours()
                                            controller.currentEdges.clear()

                                            controller.setActiveNode(None)
                                            controller.setActivePos(None)
                                            controller.setActiveItem(None)

                                            controller.setTurn(controller.getTurn()+1)

                                        # Remove placeholder relation
                                        controller.removePlaceholder()

                                        # win detection
                                        if controller.getTurn() == 3 * amount - 1:
                                            print("True")
                                            controller.done = True
                                        elif controller.getTurn() >= 2 * amount:
                                            unlockedNodes = []
                                            Check = True
                                            controller.done = False
                                            for node in controller.nodes:
                                                if len(node.relations) < 2:
                                                    Check = False
                                                    break
                                                elif len(node.relations) < 3:
                                                    unlockedNodes.append(node)
                                            if Check:
                                                for i, uNode in enumerate(unlockedNodes):
                                                    if not i == 0:
                                                        paths = pathfinding(TriangulationLogic.dt,
                                                                            [unlockedNodes[i - 1].x, unlockedNodes[i - 1].y],
                                                                            [uNode.x, uNode.y]).paths
                                                        if len(paths) > 0:
                                                            controller.done = False
                                                            break
                                                        elif i == len(unlockedNodes) - 1:
                                                            controller.done = True


                view.updateScreen()
                pygame.display.update()

# ------------------------------------------------
# Initialize classes
system = System()
view = GameView()
controller = GameController()
triLogic = TriangulationLogic()
