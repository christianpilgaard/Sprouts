import pygame, random, sys, math
from pygame.locals import *
from Triangulation import Triangulation

# TODO
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
activeItem = None
moved = False

# Node related variables
nodes = []
unlockedNodes = []
lockedNodes = []
size = 10
margin = size

# Edge related variables
edges = []
tempEdge = []

# Triangulation related variables
delauneyNodes = []
centroids = []
chosenCenter = []
centersize = 5
neighbours = []

# Game related variables
turn = 1


# ------------------------------------------------
# Node class for initializing and operating on vertices
class Node:
    def __init__(self, id, x, y, relations, locked):
        self.id = id
        self.x = x
        self.y = y
        self.relations = relations
        self.locked = locked


# ------------------------------------------------
# Edge class for initializing and operating on edges
class Edge:
    def __init__(self, pos, relations):
        self.pos = pos
        self.relations = relations


# Method for setting up initial nodes
def startGame(n):
    nodes.clear()
    angle = 0
    for i in range(n):
        x = (width / 4) * math.cos(angle * 0.0174532925)
        y = (width / 4) * math.sin(angle * 0.0174532925)
        addNode((width / 2) + x, (height / 2) + y)
        angle += 360 / n


# Method for adding vertices
def addNode(x, y):
    v = Node(len(nodes), x, y, [], False)
    nodes.append(v)
    unlockedNodes.append(v)
    delauneyNodes.append([x, y])


# Method for appending position to line
def appendPos(line, pos):
    line.append(pos)


# Method for checking whether a node
def nodeCollision(node, mousePos, type):
    color = screen.get_at(pygame.mouse.get_pos())
    if color == black and moved:
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


# Method for getting active player
def getPlayer():
    return turn % 2


# Method for checking whether the current mouse-position collides with a node or an edge
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


# Method for checking whether an edge overlaps itself
def checkEdge(tempEdge):
    seen = []
    for i, pos in enumerate(tempEdge):
        if pos in seen:
            return False
        else:
            seen.append(pos)
    return True


# Method for filling blank coordinates between two registered points in an edge
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


# Method checking if two nodes can collide
def checkNodes(node1, node2):
    return True


# Method for removing placeholder item
def removePlaceholder():
    if activeItem is not None:
        if -1 in nodes.__getitem__(activeItem).relations:
            nodes.__getitem__(activeItem).relations.remove(-1)


# Method for updating nodes
def updateNodes():
    for node in nodes:
        if len(node.relations) == 3:
            pygame.draw.circle(screen, green, (int(node.x), int(node.y)), size)
            if node not in lockedNodes:
                node.locked = True
                lockedNodes.append(node)
        else:
            pygame.draw.circle(screen, black, (int(node.x), int(node.y)), size)


# Method for updating edges
def updateEdges():
    #  for edge in edges:
    for [sPos, ePos] in edges:
        pygame.draw.line(screen, red, sPos, ePos, 5)


# Method for updating delaunay nodes
def updateCentroids():
    for [x, y] in centroids:
        pygame.draw.circle(screen, blue, (int(x), int(y)), centersize)


def updateNeighbours():
    for [x, y] in neighbours:
        pygame.draw.circle(screen, red, (int(x), int(y)), centersize)


# Method updating screen
def updateScreen():
    screen.fill(white)
    if getPlayer() == 1:
        text = font.render('1st player', True, green, blue)
    else:
        text = font.render('2nd player', True, green, blue)
    screen.blit(text, textRect)
    updateEdges()
    updateNodes()
    updateCentroids()
    updateNeighbours()


# ------------------------------------------------
# Initialize screen
pygame.init()
screen = pygame.display.set_mode((width, height), RESIZABLE)
pygame.display.set_caption("Sprouts")
background = pygame.Surface(screen.get_size())
background.fill(white)
screen.blit(background, (0, 0))
random.seed()

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)

# create a text suface object,
# on which text is drawn on it.
text = font.render('1st player', True, green, blue)

# create a rectangular object for the
# text surface object
textRect = text.get_rect()
w, h = pygame.display.get_surface().get_size()
textRect.center = (w / 2, h / 8)

screen.blit(background, (0, 0))
screen.blit(text, textRect)

# Initialize nodes
startGame(6)
dt = Triangulation()
# Insert all startnodes one by one
for s in delauneyNodes:
    dt.addPoint(s)
centroids = dt.exportCentroids()
updateCentroids()
updateNodes()

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
            if not drawing:
                for node in nodes:
                    if nodeCollision(node, mousePos, "node"):
                        if len(node.relations) < 3:
                            print(node.id, " selected.")
                            activeNode = node
                            activeItem = node.id
                            node.relations.append(-1)
                            drawing = True
                            lastPos = mousePos
                            appendPos(tempEdge, mousePos)
                            neighbours = dt.exportNeighbours([node.x, node.y], "node", chosenCenter)
                            updateNeighbours()
            else:
                for centerNode in centroids:
                    if centerNode in neighbours:
                        if nodeCollision(centerNode, mousePos, "centerNode"):
                            if lastPos is not None:
                                if lastPos != mousePos:
                                    edges.append([lastPos, mousePos])
                                    chosenCenter.append(centerNode)
                                    neighbours = dt.exportNeighbours(centerNode, "centerNode", chosenCenter)
                                    #remove startnode, if there are only chosen 1 centroid = no loop
                                    if ([activeNode.x, activeNode.y] in neighbours) and (len(chosenCenter) < 2):
                                        neighbours.remove([activeNode.x, activeNode.y])
                                    for node in nodes:
                                        for n in neighbours:
                                            if ([node.x, node.y] == n) and node.locked:
                                                neighbours.remove([node.x, node.y])
                                    updateNodes()
                                    updateCentroids()
                                    updateNeighbours()

                                    lastPos = mousePos
                for node in nodes:
                    if nodeCollision(node, mousePos, "node"):
                        if [node.x, node.y] in neighbours:
                            if len(node.relations) < 3:
                                if lastPos is not None:
                                    if lastPos != mousePos:
                                        edges.append([lastPos, mousePos])

                                        if len(chosenCenter) > 0:
                                            mid = chosenCenter[int(len(chosenCenter) / 2)]
                                        else:
                                            mid = [(lastPos[0] + mousePos[0]) / 2, (lastPos[1] + mousePos[1]) / 2]
                                        addNode(mid[0], mid[1])
                                        tempEdge = []

                                        # Remove placeholder relation
                                        nodes.__getitem__(activeItem).relations.remove(-1)

                                        # Add relations between connected nodes
                                        nodes.__getitem__(activeItem).relations.append(nodes[-1].id)
                                        nodes.__getitem__(node.id).relations.append(nodes[-1].id)
                                        nodes.__getitem__(-1).relations.append(activeItem)
                                        nodes.__getitem__(-1).relations.append(node.id)

                                        # Add new path and node
                                        dt.addPath([activeNode.x, activeNode.y], [node.x, node.y], chosenCenter, mid)
                                        # Update centroids
                                        centroids = dt.exportCentroids()
                                        chosenCenter.clear()
                                        neighbours.clear()

                                        activeNode = None
                                        activeItem = None
                                        lastPos = None

                                        # Change turn
                                        turn += 1

                            # Reset current drawing
                            moved = False
                            drawing = False

                            # Remove placeholder relation
                            removePlaceholder()

                            # Update screen
                            updateScreen()

            if not drawing:
                # Reset current drawing
                lastPos = None
                moved = False
                drawing = False
                tempEdge = []

                # Remove placeholder relation
                removePlaceholder()

                # Update screen
                updateScreen()

    # Update
    pygame.display.update()
