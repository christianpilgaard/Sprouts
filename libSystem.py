import math
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

    # Font
    font = None
    back_button = None
    restart_button = None

    # Screen
    screen = pygame.display.set_mode((width, height), RESIZABLE)
    background = pygame.Surface(screen.get_size())

    def init(self):
        print("System initialized.")
        pygame.init()
        pygame.display.set_caption("Sprouts")
        self.background.fill(self.white)
        self.screen.blit(self.background, (0, 0))
        random.seed()

        self.font = pygame.font.SysFont(None, 40)
        self.back_button = pygame.Rect(20, 20, 100, 50)
        self.restart_button = pygame.Rect(140, 20, 100, 50)

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

    def getGreen(self):
        return self.green

    def getBlue(self):
        return self.blue

    def getGray(self):
        return self.gray

    def getScreen(self):
        return self.screen

    def getBackground(self):
        return self.background

    def fillWhite(self):
        self.screen.fill(self.getWhite())

    # Method for updating drawn path
    def updatePath(self, lastPos, mousePos):
        pygame.draw.line(self.getScreen(), self.getBlue(), lastPos, mousePos, 5)

    # Method for updating nodes
    def updateNodes(self, nodes, size):
        for node in nodes:
            if len(node.relations) == 3:
                pygame.draw.circle(self.getScreen(), self.getGreen(), (int(node.x), int(node.y)), size)
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
            pygame.draw.line(self.getScreen(), self.getGray(), dEdge.start.coordinates, dEdge.end.coordinates, size)

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
        self.updateNeighbours(neighbours, size)
        self.updateNodes(nodes, size)
        self.displayPlayer(player)

    # Player
    def displayPlayer(self, player):
        if player == 1:
            self.drawText('Player 1', self.font, self.getBlue(), self.getScreen(), self.getHeight() / 2, self.getWidth() / 20)
        elif player == 2:
            self.drawText('Player 2', self.font, self.getRed(), self.getScreen(), self.getHeight() / 2, self.getWidth() / 20)

    def displayWinner(self, player):
        if player == 1:
            return self.drawPopUp('Player 2 wins!'.format())
        elif player == 2:
            return self.drawPopUp('Player 1 wins!'.format())

    # Method for drawing text on the screen
    def drawText(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def drawGUI(self):
        pygame.draw.rect(self.getScreen(), self.getBlack(), self.back_button)
        self.drawText('back', self.font, self.getWhite(), self.getScreen(), 70, 45)
        pygame.draw.rect(self.getScreen(), self.getBlack(), self.restart_button)
        self.drawText('restart', self.font, self.getWhite(), self.getScreen(), 190, 45)

    def drawPopUp(self, text):
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pupup_frame = pygame.Rect(195, 295, 410, 210)
        popup = pygame.Rect(200, 300, 400, 200)
        popup_button = pygame.Rect(350, 425, 100, 50)
        pygame.draw.rect(self.getScreen(), (0, 0, 0), pupup_frame)
        pygame.draw.rect(self.getScreen(), (255, 255, 255), popup)
        if popup_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(system.screen, (0, 150, 0), popup_button)
            if click:
                return True
        else:
            pygame.draw.rect(self.getScreen(), (0, 0, 0), popup_button)
        self.drawText(text, self.font, (0, 0, 0), self.getScreen(), 400, 350)
        self.drawText('Close', self.font, (255, 255, 255), self.getScreen(), 400, 450)
