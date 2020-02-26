import pygame, random, sys
from pygame.locals import *

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
gray = 150, 150, 150

# Drawing variables
drawing = False
lastPos = None
activePoint = None

def makePoint(x, y):
    point = (int(x), int(y), 0)
    points.append(point)


def startGame(p):
    points.clear()
    if p == 2:
        makePoint(1 * width / 3, 1 * height / 2)
        makePoint(2 * width / 3, 1 * height / 2)
    if p == 3:
        rand = random.randint(0, 1)
        if rand > 0.5:
            makePoint(1 * width / 2, 1 * height / 3)
            makePoint(2 * width / 3, 2 * height / 3)
            makePoint(1 * width / 3, 2 * height / 3)
        else:
            makePoint(1 * width / 3, 1 * height / 2)
            makePoint(1 * width / 2, 1 * height / 2)
            makePoint(2 * width / 3, 1 * height / 2)


points = []
size = width, height = 500, 500
startGame(3)

pygame.init()

screen = pygame.display.set_mode((width, height), RESIZABLE)
# screen = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN, depth=0, display=0)
pygame.display.set_caption("Sprouts")
global background
background = pygame.Surface(screen.get_size())
background.fill(white)
screen.blit(background, (0, 0))
pygame.display.flip()
random.seed()

[(1, 1, 0), (2, 2, 0)]

while 1:
    for event in pygame.event.get():
        mousePos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

        # Select point
        elif event.type == MOUSEBUTTONDOWN:

            # Check if mousePos is in points with select margin
            for i in points:
                if ((abs(mousePos[0] - i[0])) < 10) & ((abs(mousePos[1] - i[1])) < 10):
                    print(i, " selected.")
                    activePoint = i
                    drawing = True

        # Draw freehand from active point
        elif drawing:
            if lastPos is not None:
                pygame.draw.line(screen, black, lastPos, mousePos, 1)
            lastPos = mousePos

            # Check if mousePos is in points with select margin
            for i in points:
                if i == activePoint:
                    print(i)

                elif ((abs(mousePos[0] - i[0])) < 10) & ((abs(mousePos[1] - i[1])) < 10):
                    print(i, " selected.")
                    drawing = False

    # Draw points as rectangles
    for i in points:
        pygame.draw.rect(screen, black, (i[0], i[1], 5, 5))

    pygame.display.flip()