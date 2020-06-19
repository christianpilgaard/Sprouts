import math
import pygame, random, sys, math
import numpy as np
from pygame.locals import *


# -------------------- ----------------------------
# System class
class System:

    def __init__(self, width, height):
        # System related variables
        self.width = width
        self.height = height
        # Color definitions
        self.black = 0, 0, 0
        self.white = 255, 255, 255
        self.red = 255, 0, 0
        self.lgreen = 0, 255, 0
        self.dgreen = 0, 150, 0
        self.blue = 0, 0, 150
        self.gray = 150, 150, 150
        # Font
        self.fontSmall = pygame.font.SysFont(None, 24)
        self.fontMedium = pygame.font.SysFont(None, 40)
        self.fontBig = pygame.font.SysFont(None, 100)
        # Buttons
        self.backButton = pygame.Rect(20, 20, 100, 50)
        self.restartButton = pygame.Rect(140, 20, 100, 50)
        # Screen
        self.screen = pygame.display.set_mode((width, height), RESIZABLE)
        pygame.display.set_caption('Sprouts')
        # FPS
        self.mainClock = pygame.time.Clock()

    def init(self):
        pygame.init()
        pygame.display.set_caption("Sprouts")
        self.getScreen().fill(self.getWhite())

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getBlack(self):
        return self.black

    def getWhite(self):
        return self.white

    def getRed(self):
        return self.red

    def getLGreen(self):
        return self.lgreen

    def getDGreen(self):
        return self.dgreen

    def getBlue(self):
        return self.blue

    def getGray(self):
        return self.gray

    def getFontSmall(self):
        return self.fontSmall

    def getFontMedium(self):
        return self.fontMedium

    def getFontBig(self):
        return self.fontBig

    def getBackButton(self):
        return self.backButton

    def getRestartButton(self):
        return self.restartButton

    def getScreen(self):
        return self.screen

    def setScreen(self, screen):
        self.screen = screen

    def getMainClock(self):
        return self.mainClock

    def fillWhite(self):
        self.screen.fill(self.getWhite())

    # Method for updating drawn path
    def updatePath(self, lastPos, mousePos):
        pygame.draw.line(self.getScreen(), self.getBlue(), lastPos, mousePos, 5)

    # Method for updating nodes
    def updateNodes(self, nodes, size):
        for node in nodes:
            if len(node.getRelations()) == 3:
                pygame.draw.circle(self.getScreen(), self.getLGreen(), (int(node.x), int(node.y)), size)
            else:
                pygame.draw.circle(self.getScreen(), self.getBlack(), (int(node.x), int(node.y)), size)

    # Method for updating edges
    def updateEdges1(self, edges, thickness):
        for edge in edges:
            for i, pos in enumerate(edge):
                if i - 1 != -1:
                    pygame.draw.line(self.getScreen(), self.getRed(), edge[i - 1], pos, thickness)

    # Method for updating edges
    def updateEdges2(self, edges, thickness):
        for [sPos, ePos] in edges:
            pygame.draw.line(self.getScreen(), self.getRed(), sPos, ePos, thickness)

    # Method for updating delaunay nodes
    def updateCentroids(self, centroids, size):
        for [x, y] in centroids:
            pygame.draw.circle(self.getScreen(), self.getBlue(), (int(x), int(y)), size)

    def updateTriLines(self, triEdges, size):
        for dEdge in triEdges:
            pygame.draw.line(self.getScreen(), self.getGray(), dEdge.getStart().getCoordinates(), dEdge.getEnd().getCoordinates(), size)

    def updateNeighbours(self, neighbours, size):
        for [x, y] in neighbours:
            pygame.draw.circle(self.getScreen(), self.getRed(), (int(x), int(y)), size)

    # Method updating screen
    def updateScreen1(self, fill, nodes, edges, size, thickness, player):
        if fill:
            self.fillWhite()
        self.updateEdges1(edges, thickness)
        self.updateNodes(nodes, size)
        self.drawGUI()
        self.displayPlayer(player)

    # Method updating screen
    def updateScreen2(self, nodes, edges, centroids, triEdges, neighbours, size, cenSize, thickness, player):
        self.fillWhite()
        self.drawGUI()
        self.updateTriLines(triEdges, thickness)
        self.updateEdges2(edges, thickness)
        self.updateCentroids(centroids, cenSize)
        self.updateNeighbours(neighbours, 12)
        self.updateNodes(nodes, size)
        self.displayPlayer(player)

    # Player
    def displayPlayer(self, player):
        if player == 1:
            self.drawText('Player 1', self.getFontMedium(), self.getBlue(), self.getScreen(), self.getHeight() / 2, self.getWidth() / 20)
        elif player == 2:
            self.drawText('Player 2', self.getFontMedium(), self.getRed(), self.getScreen(), self.getHeight() / 2, self.getWidth() / 20)

    def displayWinner(self, player):
        if player == 1:
            return self.drawPopUp('Player 2 wins!')
        elif player == 2:
            return self.drawPopUp('Player 1 wins!')

    # Method for drawing text on the screen
    def drawText(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def drawGUI(self):
        pygame.draw.rect(self.getScreen(), self.getBlack(), self.getBackButton())
        self.drawText('back', self.getFontMedium(), self.getWhite(), self.getScreen(), 70, 45)
        pygame.draw.rect(self.getScreen(), self.getBlack(), self.getRestartButton())
        self.drawText('restart', self.getFontMedium(), self.getWhite(), self.getScreen(), 190, 45)

    def drawPopUp(self, text):
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pupupFrame = pygame.Rect(195, 295, 410, 210)
        popup = pygame.Rect(200, 300, 400, 200)
        popupButton = pygame.Rect(350, 425, 100, 50)
        pygame.draw.rect(self.getScreen(), self.getBlack(), pupupFrame)
        pygame.draw.rect(self.getScreen(), self.getWhite(), popup)
        if popupButton.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.getScreen(), self.getDGreen(), popupButton)
            if click:
                return True
        else:
            pygame.draw.rect(self.getScreen(), self.getBlack(), popupButton)
        self.drawText(text, self.getFontSmall(), self.getBlack(), self.getScreen(), 400, 350)
        self.drawText('Close', self.getFontMedium(), self.getWhite(), self.getScreen(), 400, 450)
