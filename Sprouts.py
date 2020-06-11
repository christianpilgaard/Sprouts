import pygame, random, sys, math
from pygame.locals import *

# TODO
# - Fix that you don't have to click twice on "back"-button (Den ved at knappen klikkes på, men den returnerer fra noget andet)
# - Fix that nodes doesn't always connect when they are supposed to
# - Fix "IndexError" with line: "addNode(int(tempEdge[mid][0]), int(tempEdge[mid][1]))"

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

# Node related variables
nodes = []
unlockedNodes = []
lockedNodes = []
size = 20
margin = size

# Edge related variables
edges = []
edge = []
tempEdge = []


# ------------------------------------------------
# Node class for initializing and operating on vertices
class Node:
    def __init__(self, id, x, y, relations, locked):
        self.id = id
        self.x = x
        self.y = y
        self.relations = relations
        self.locked = locked

# Method for setting up initial nodes
def startGame(n):
    screen.fill(white)
    # create a rectangular object for the
    # text surface object
    nodes.clear()
    edges.clear()
    angle = 0
    for i in range(n):
        x = (width/4) * math.cos(angle*0.0174532925)
        y = (width/4) * math.sin(angle*0.0174532925)
        addNode((width/2)+x, (height/2)+y)
        angle += 360/n
    updateScreen(1)
    return playGame(n)


# Method for adding vertices
def addNode(x, y):
    v = Node(len(nodes), x, y, [], False)
    nodes.append(v)
    unlockedNodes.append(v)


# Method for appending position to line
def appendPos(line, pos):
    line.append(pos)


# Method for checking whether a node
def nodeCollision(node, mousePos, moved):

    color = screen.get_at(pygame.mouse.get_pos())
    if color == black and moved:
        return False

    if not ((abs(mousePos[0] - node.x)) < margin) & ((abs(mousePos[1] - node.y)) < margin):
        return False
    return True


# Method for checking a position has reached a certain distance away from a node
def reverseNodeCollision(node, mousePos):
    if not ((abs(mousePos[0] - node.x)) > size) & ((abs(mousePos[1] - node.y)) > size):
        return False
    return True


# Method for getting active player
def getPlayer(turn):
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
def removePlaceholder(activeItem):
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
    for edge in edges:
        for i, pos in enumerate(edge):
            if i - 1 != -1:
                pygame.draw.line(screen, red, edge[i - 1], pos, 5)


# Method updating screen
def updateScreen(turn):
    screen.fill(white)
    if getPlayer(turn) == 1:
        draw_text('Player 1', font_n, blue, screen, height/2, width/20)
    else:
        draw_text('Player 2', font_n, red, screen, height/2, width/20)
    pygame.draw.rect(screen, black, back_button)
    draw_text('back', font_n, white, screen, 70, 45)
    pygame.draw.rect(screen, black, restart_button)
    draw_text('restart', font_n, white, screen, 190, 45)
    updateEdges()
    updateNodes()

# Method for drawing text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


def playGame(n):
    # Drawing related variables
    drawing = False
    lastPos = None
    activeNode = None
    moved = False
    tempEdge = []
    # Game related variables
    turn = 1
    # Game loop -----------------------------
    while 1:
        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()

            # Quit game
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 0

            # Select node -----------------------------
            # Mouse 1 for drawing
            elif event.type == MOUSEBUTTONDOWN:
                for node in nodes:
                    if nodeCollision(node, mousePos, moved):
                        if len(node.relations) < 3:
                            activeNode = node
                            activeItem = node.id
                            node.relations.append(-1)
                            drawing = True
                            lastPos = mousePos
                            edges.append([])
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    return 0
                elif restart_button.collidepoint(pygame.mouse.get_pos()):
                    return 1

            # Draw from node -----------------------------
            if drawing:
                if lastPos is not None:
                    if lastPos != mousePos:
                        pygame.draw.line(screen, blue, lastPos, mousePos, 5)
                        fillBlank(lastPos, mousePos)
                        appendPos(tempEdge, mousePos)
                lastPos = mousePos

                # Check if any node or line is hit -----------------------------
                # Avoid initially targeting active point
                if not moved:
                    pass
                    if reverseNodeCollision(nodes.__getitem__(activeItem), mousePos):
                        moved = True
                else:
                    # Check for hit detection while drawing
                    for i, node in enumerate(nodes):
                        if nodeCollision(node, mousePos, moved):
                            if len(node.relations) < 3:
                                # Append an edge connecting the nodes
                                # Add new node on edge

                                if checkEdge(tempEdge):
                                    edges.append(tempEdge)
                                    mid = int(len(tempEdge) / 2)
                                    addNode(int(tempEdge[mid+1][0]), int(tempEdge[mid+1][1]))
                                    tempEdge = []

                                    # Remove placeholder relation
                                    nodes.__getitem__(activeItem).relations.remove(-1)

                                    # Add relations between connected nodes
                                    nodes.__getitem__(activeItem).relations.append(nodes[-1].id)
                                    nodes.__getitem__(node.id).relations.append(nodes[-1].id)
                                    nodes.__getitem__(-1).relations.append(activeItem)
                                    nodes.__getitem__(-1).relations.append(node.id)
                                    activeNode = None
                                    activeItem = None

                                    # Change turn
                                    turn += 1

                            # Reset current drawing
                            lastPos = None
                            moved = False
                            drawing = False

                            # Remove placeholder relation
                            removePlaceholder(activeItem)

                            # Update screen
                            updateScreen(turn)
                drawing = checkCollision()
                if not drawing:
                    # Reset current drawing
                    lastPos = None
                    moved = False
                    drawing = False
                    tempEdge = []

                    # Remove placeholder relation
                    removePlaceholder(activeItem)

                    # Update screen
                    updateScreen(turn)

        # Update
        updateNodes()
        pygame.display.update()

# ------------------------------------------------
# Initialize screen
pygame.init()
screen = pygame.display.set_mode((width, height), RESIZABLE)
pygame.display.set_caption("Sprouts")
background = pygame.Surface(screen.get_size())
background.fill(white)
screen.blit(background, (0, 0))
random.seed()

font_n = pygame.font.SysFont(None, 40)
back_button = pygame.Rect(20, 20, 100, 50)
restart_button = pygame.Rect(140, 20, 100, 50)
