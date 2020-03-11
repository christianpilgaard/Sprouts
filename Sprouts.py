import pygame, random, sys
from pygame.locals import *

# TODO
# - Fix anchoring
# - Add restriction if node is drawn to itself
# - Make fillBlank-method prettier

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

# Drawing related variables
drawing = False
lastPos = None
activeNode = None
moved = False
margin = 20

# Node related variables
nodes = []
size = 20

# Edge related variables
edges = []
edge = []
tempEdge = []


# ------------------------------------------------
# Vertex class for initializing and operating on vertices
class Node:
    def __init__(self, id, x, y, relations):
        self.id = id
        self.x = x
        self.y = y
        self.relations = relations


# Method for adding vertices
def addNode(x, y):
    v = Node(len(nodes), x, y, [])
    nodes.append(v)


def updateNodes():
    for node in nodes:
        if len(node.relations) == 3:
            pygame.draw.circle(screen, green, (int(node.x), int(node.y)), size)
        else:
            pygame.draw.circle(screen, black, (int(node.x), int(node.y)), size)


def updateEdges():
    for edge in edges:
        pos = None
        cPos = None
        for i in edge:
            pygame.draw.line(screen, black, i[0], i[1], 5)


# Method for setting up initial nodes
def startGame(p):
    nodes.clear()
    if p == 2:
        addNode(1 * width / 3, 1 * height / 2)
        addNode(2 * width / 3, 1 * height / 2)
    rand = random.randint(0, 1)
    if p == 3:
        rand = random.randint(0, 1)
        if rand > 0.5:
            addNode(1 * width / 2, 1 * height / 3)
            addNode(2 * width / 3, 2 * height / 3)
            addNode(1 * width / 3, 2 * height / 3)
        else:
            addNode(1 * width / 4, 1 * height / 2)
            addNode(2 * width / 4, 1 * height / 2)
            addNode(3 * width / 4, 1 * height / 2)
    elif p == 4:
        if rand > 0.5:
            addNode(2 * width / 5, 2 * height / 5)
            addNode(4 * width / 5, 2 * height / 5)
            addNode(2 * width / 5, 4 * height / 5)
            addNode(4 * width / 5, 4 * height / 5)
        else:
            addNode(2 * width / 9, 2 * height / 5)
            addNode(6 * width / 9, 2 * height / 5)
            addNode(4 * width / 9, 4 * height / 5)
            addNode(8 * width / 9, 4 * height / 5)
    elif p == 5:
        if rand > 0.5:
            addNode(2 * width / 5, 2 * height / 5)
            addNode(4 * width / 5, 2 * height / 5)
            addNode(2 * width / 5, 4 * height / 5)
            addNode(4 * width / 5, 4 * height / 5)
            addNode(3 * width / 5, 3 * height / 5)
        else:
            addNode(4 * width / 7, 2 * height / 7)
            addNode(2 * width / 7, 3 * height / 7)
            addNode(6 * width / 7, 3 * height / 7)
            addNode(3 * width / 7, 5 * height / 7)
            addNode(5 * width / 7, 5 * height / 7)


def appendPos(line, pos):
    line.append(pos)


def drawLines():
    for edge in edges:
        for i, pos in enumerate(edge):
            if i - 1 != -1:
                pygame.draw.line(screen, red, edge[i - 1], pos, 5)


def checkCollision():
    color = screen.get_at(pygame.mouse.get_pos())
    if color == red:
        return False
    else:
        currPos = pygame.mouse.get_pos()

        for pos in tempEdge:
            if pos[0] == currPos:
                return False
    return True


def fillBlank(pos1, pos2):
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
        tempEdge.append(new_posX)
    if new_posY != ():
        tempEdge.append(new_posY)

    if new_pos != pos2 and new_pos != ():
        fillBlank(new_pos, pos2)


def wipe():
    screen.fill(white)
    drawLines()
    updateNodes()

# ------------------------------------------------
# Initialize screen
pygame.init()
screen = pygame.display.set_mode((width, height), RESIZABLE)
pygame.display.set_caption("Sprouts")
background = pygame.Surface(screen.get_size())
background.fill(white)
screen.blit(background, (0, 0))
random.seed()

# Initialize nodes
startGame(5)

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

        # Select node -----------------------------
        # Mouse 1 for drawing
        elif event.type == MOUSEBUTTONDOWN:
            for node in nodes:
                if ((abs(mousePos[0] - node.x)) < margin) & ((abs(mousePos[1] - node.y)) < margin):
                    if len(node.relations) < 3:
                        print(node.id, " selected.")
                        activeNode = node
                        activeItem = node.id
                        drawing = True
                        lastPos = mousePos
                        edges.append([])

        # Draw from node -----------------------------
        if drawing:
            drawing = checkCollision()
            if lastPos is not None:
                if lastPos != mousePos:
                    pygame.draw.line(screen, black, lastPos, mousePos, 5)
                    fillBlank(lastPos, mousePos)
                    appendPos(tempEdge, mousePos)
            lastPos = mousePos

            # Check if any node or line is hit -----------------------------
            # Avoid initially targeting active point
            if not moved:
                if ((abs(mousePos[0] - activeNode.x)) > margin) & ((abs(mousePos[1] - activeNode.y)) > margin):
                    moved = True
            else:
                # Check for hit detection while drawing
                for i, node in enumerate(nodes):
                    if (abs(mousePos[0] - (node.x + (size/2))) < margin-10) & ((abs(mousePos[1] - (node.y + (size / 2)))) < margin - 10):
                        if len(node.relations) < 3:
                            # Append an edge connecting the nodes
                            # Add new node on edge
                            edges.append(tempEdge)
                            mid = int(len(tempEdge) / 2)
                            addNode(int(tempEdge[mid][0]), int(tempEdge[mid][1]))
                            tempEdge = []

                            # Add relations between connected nodes
                            nodes.__getitem__(activeItem).relations.append(nodes[-1].id)
                            nodes.__getitem__(node.id).relations.append(nodes[-1].id)
                            nodes.__getitem__(-1).relations.append(activeItem)
                            nodes.__getitem__(-1).relations.append(node.id)
                            activeNode = None
                            activeItem = None

                        # Reset current drawing
                        lastPos = None
                        moved = False
                        drawing = False

                        # Print node relations
                        for node in nodes:
                            print(node.id, ": ", node.relations)

                        # Reset
                        wipe()

            if not drawing:
                lastPos = None
                tempEdge = []
                wipe()


    # Update
    updateNodes()
    pygame.display.update()

