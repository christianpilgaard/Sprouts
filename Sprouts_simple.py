import pygame, random, sys, math
import numpy as np
from pygame.locals import *


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
# Game controller class
class GameController:

    # Node related variables
    nodes = []
    size = 15
    edges = []
    tempEdge = []

    # Drawing related variables
    activeNode = None
    activeItem = None
    activePos = None
    mousePos = None
    drawing = False
    lastPos = None
    moved = False

    # Method for adding vertices
    def addNode(self, x, y):
        v = Node(len(self.nodes), x, y, [], False, False)
        self.nodes.append(v)

    def getNodes(self):
        return self.nodes

    def getEdges(self):
        return self.edges

    def getDrawing(self):
        return self.drawing

    def getLastPos(self):
        return self.lastPos

    def getMousePos(self):
        return self.mousePos

    def getMoved(self):
        return self.moved

    def getTempEdge(self):
        return self.tempEdge

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

    def resetGame(self):
        self.nodes.clear()
        self.edges.clear()
        self.activePos = None
        self.activeItem = None
        self.activeNode = None
        self.mousePos = None
        self.drawing = False
        self.lastPos = None
        self.moved = False

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
            dx = node.x - mousePos[0]
            dy = node.y - mousePos[1]
            dis = math.sqrt(dx ** 2 + dy ** 2)
            print("dis", dis, "dx", dx, "dy", dy)
            if dis < controller.size:

                return True
            return False
        elif type == "node2":
            if not ((abs(mousePos[0] - node.x)) < self.size) & ((abs(mousePos[1] - node.y)) < self.size):
                return False
            return True
        else:
            if not ((abs(mousePos[0] - node[0])) < self.size) & ((abs(mousePos[1] - node[1])) < self.size):
                return False
            return True

    # Method for checking a position has reached a certain distance away from a node
    def reverseNodeCollision(self, node, mousePos):
        dx = node.x - mousePos[0]
        dy = node.y - mousePos[1]
        dis = math.sqrt(dx ** 2 + dy ** 2)
        if dis < controller.size+10:
            return False
        return True

    # Method for checking whether the current mouse-position collides with a node or an edge
    def checkCollision(self):
        color = system.screen.get_at(pygame.mouse.get_pos())
        if color == system.red:
            return False
        else:
            currPos = pygame.mouse.get_pos()
            for pos in self.tempEdge:
                if pos[0] == currPos:
                    return False
        return True

    # Method for checking whether an edge overlaps itself
    def checkEdge(self, tempEdge):
        seen = []
        for i, pos in enumerate(tempEdge):
            if pos in seen:
                return False
            else:
                seen.append(pos)
        return True

    # Method for removing placeholder item
    def removePlaceholder(self):
        if self.getActiveItem() is not None:
            if -1 in self.getNodes().__getitem__(self.getActiveItem()).relations:
                self.nodes.__getitem__(self.getActiveItem()).relations.remove(-1)

    # Method for filling blank coordinates between two registered points in an edge
    def fillBlank(self, pos1, pos2):
        # ADD TO X AND ADD TO Y
        new_posX = ()
        new_posY = ()
        new_pos = ()
        if pos2[0] - pos1[0] > 1 and pos2[1] - pos1[1] > 1:
            new_posX = (pos1[0] + 1, pos1[1])
            new_posY = (pos1[0], pos1[1] + 1)
            new_pos = (pos1[0] + 1, pos1[1] + 1)

        # ADD TO X AND SUBTRACT FROM Y
        elif pos2[0] - pos1[0] > 1 and pos1[1] - pos2[1] > 1:
            new_posX = (pos1[0] + 1, pos1[1])
            new_posY = (pos1[0], pos1[1] - 1)
            new_pos = (pos1[0] + 1, pos1[1] - 1)
        # SUBTRACT FROM X AND ADD TO Y
        elif pos1[0] - pos2[0] > 1 and pos2[1] - pos1[1] > 1:
            new_posX = (pos1[0] - 1, pos1[1])
            new_posY = (pos1[0], pos1[1] + 1)
            new_pos = (pos1[0] - 1, pos1[1] + 1)
        # SUBTRACT FROM X AND SUBTRACT FROM Y
        elif pos1[0] - pos2[0] > 1 and pos1[1] - pos2[1] > 1:
            new_posX = (pos1[0] - 1, pos1[1])
            new_posY = (pos1[0], pos1[1] - 1)
            new_pos = (pos1[0] - 1, pos1[1] - 1)
        # ADD TO X
        elif pos2[0] - pos1[0] > 1:
            new_posX = (pos1[0] + 1, pos1[1])
            new_pos = new_posX
        # SUBTRACT FROM X
        elif pos1[0] - pos2[0] > 1:
            new_posX = (pos1[0] - 1, pos1[1])
            new_pos = new_posX
        # ADD TO Y
        elif pos2[1] - pos1[1] > 1:
            new_posY = (pos1[0], pos1[1] + 1)
            new_pos = new_posY
        # SUBTRACT FROM Y
        elif pos1[1] - pos2[1] > 1:
            new_posY = (pos1[0], pos1[1] - 1)
            new_pos = new_posY

        if new_posX != ():
            self.tempEdge.append(new_posX)
        if new_posY != ():
            self.tempEdge.append(new_posY)

        if new_pos != pos2 and new_pos != ():
            self.fillBlank(new_pos, pos2)


# ------------------------------------------------
# Game view class
class GameView:

    # Method for updating nodes
    def updateNodes(self):
        for node in controller.getNodes():
            if len(node.relations) == 3:
                pygame.draw.circle(system.screen, system.green, (int(node.x), int(node.y)), controller.size)
            else:
                pygame.draw.circle(system.screen, system.black, (int(node.x), int(node.y)), controller.size)

    # Method for updating edges
    def updateEdges(self):
        for edge in controller.edges:
            for i, pos in enumerate(edge):
                if i - 1 != -1:
                    pygame.draw.line(system.screen, system.red, edge[i - 1], pos, 5)

    def updatePath(self, lastPos, mousePos):
        pygame.draw.line(system.screen, system.blue, lastPos, mousePos, 5)

    # Method updating screen
    def updateScreen(self):
        system.screen.fill(system.white)
        view.updateEdges()
        view.updateNodes()


# -------------------------------------------------------------------
# --------------------------- MAIN GAME -----------------------------
# -------------------------------------------------------------------
def playGame(amount):
    controller.resetGame()

    # Initialize game
    system.init()
    controller.startGame(amount)
    controller.drawing = False

    # Game loop -----------------------------
    while 1:
        for event in pygame.event.get():
            controller.mousePos = pygame.mouse.get_pos()

            # Quit game
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_BACKSPACE:
                    return
                elif event.key == K_SPACE:
                    print("Space")

            # Select node -----------------------------
            # Mouse 1 for drawing
            elif event.type == MOUSEBUTTONDOWN:
                for node in controller.getNodes():
                    if controller.nodeCollision(node, controller.getMousePos(), "node"):
                        if len(node.relations) < 3:
                            print(node.id, " selected.")
                            controller.setActiveNode(node)
                            controller.setActiveItem(node.id)
                            controller.setActivePos([controller.getActiveNode().x, controller.getActiveNode().y])
                            node.relations.append(-1)
                            controller.drawing = True
                            controller.lastPos = controller.getMousePos()

            # Draw from node ---------------------------
            if controller.getDrawing():
                controller.drawing = controller.checkCollision()
                if controller.getLastPos() is not None:
                    if controller.getLastPos() != controller.getMousePos():
                        view.updatePath(controller.getLastPos(), controller.getMousePos())
                        controller.fillBlank(controller.getLastPos(), controller.getMousePos())
                        controller.tempEdge.append(controller.getMousePos())
                controller.lastPos = controller.getMousePos()

                # Check if any node or line is hit -----------------------------
                # Avoid initially targeting active point
                if not controller.getMoved():
                    if controller.reverseNodeCollision(controller.getNodes().__getitem__(controller.getActiveItem()), controller.getMousePos()):
                        controller.moved = True

                else:
                    # Check for hit detection while drawing
                    for i, node in enumerate(controller.getNodes()):
                        if controller.nodeCollision(node, controller.getMousePos(), "node"):
                            if len(node.relations) < 3:
                                # Append an edge connecting the nodes
                                # Add new node on edge

                                if controller.checkEdge(controller.getTempEdge()):

                                    controller.edges.append(controller.tempEdge)
                                    mid = int(len(controller.getTempEdge()) / 2)
                                    controller.addNode(int(controller.getTempEdge()[mid][0]), int(controller.getTempEdge()[mid][1]))
                                    controller.tempEdge = []

                                    # Remove placeholder relation
                                    controller.getNodes().__getitem__(controller.getActiveItem()).relations.remove(-1)

                                    # Add relations between connected nodes
                                    controller.getNodes().__getitem__(controller.getActiveItem()).relations.append(controller.getNodes()[-1].id)
                                    controller.getNodes().__getitem__(node.id).relations.append(controller.getNodes()[-1].id)
                                    controller.getNodes().__getitem__(-1).relations.append(controller.getActiveItem())
                                    controller.getNodes().__getitem__(-1).relations.append(node.id)
                                    controller.activeNode = None
                                    controller.activeItem = None

                            # Reset current drawing
                            controller.lastPos = None
                            controller.moved = False
                            controller.drawing = False

                            # Remove placeholder relation
                            controller.removePlaceholder()

                            # Update screen
                            view.updateScreen()

                if not controller.getDrawing():
                    # Reset current drawing
                    controller.lastPos = None
                    controller.moved = False
                    controller.drawing = False
                    controller.tempEdge = []

                    # Remove placeholder relation
                    controller.removePlaceholder()

                    # Update screen
                    view.updateScreen()

        view.updateEdges()
        view.updateNodes()
        pygame.display.update()


# ------------------------------------------------
# Initialize classes
view = GameView()
system = System()
controller = GameController()