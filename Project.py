import pygame, random, sys
from pygame.locals import *

black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255
gray = 150,150,150


def makePoint (x,y):
    point = (int(x),int(y),0)
    points.append(point)

def startGame (p):
    points.clear()
    if p == 2:
        makePoint(1*width/3,1*height/2)
        makePoint(2*width/3,1*height/2)
    rand = random.randint(0,1)
    if p == 3:
        rand = random.randint(0,1)
        if rand > 0.5:
            makePoint(1*width/2,1*height/3)
            makePoint(2*width/3,2*height/3)
            makePoint(1*width/3,2*height/3)
        else:
            makePoint(1*width/4,1*height/2)
            makePoint(2*width/4,1*height/2)
            makePoint(3*width/4,1*height/2)
    elif p == 4:
        if rand > 0.5:
            makePoint(2*width/5,2*height/5)
            makePoint(4*width/5,2*height/5)
            makePoint(2*width/5,4*height/5)
            makePoint(4*width/5,4*height/5)
        else:
            makePoint(2*width/9,2*height/5)
            makePoint(6*width/9,2*height/5)
            makePoint(4*width/9,4*height/5)
            makePoint(8*width/9,4*height/5)
    elif p == 5:
        if rand > 0.5:
            makePoint(2*width/5,2*height/5)
            makePoint(4*width/5,2*height/5)
            makePoint(2*width/5,4*height/5)
            makePoint(4*width/5,4*height/5)
            makePoint(3*width/5,3*height/5)
        else:
            makePoint(4*width/7,2*height/7)
            makePoint(2*width/7,3*height/7)
            makePoint(6*width/7,3*height/7)
            makePoint(3*width/7,5*height/7)
            makePoint(5*width/7,5*height/7)

def drawPoints():
    for content in points:
        pygame.draw.circle(screen, black, (content[0],content[1]),20)

def appendPos(line, pos):
    line.append(pos)

def drawLines():
    for content in lines:
        for i, pos in enumerate(content):
            if i-1 != -1:
                pygame.draw.line(screen, red, content[i-1], pos, 5)

def checkCollision():
    color = screen.get_at(pygame.mouse.get_pos())
    if color == red:
        return False
    else:
        currPos = pygame.mouse.get_pos()

        for pos in templine:
            if pos[0] == currPos:
                return False
    return True

def fillBlank(pos1,pos2):
    if pos2[0] - pos1[0] > 1:
        length = pos2[0] - pos1[0]-1
        for i in range(length):
            print("1 Insert:", (pos1[0]+i+1,pos1[1]))
            templine.append((pos1[0]+i+1,pos1[1]))
    #if pos1[0] - pos2[0] > 1:
    #    length = pos1[0] - pos2[0]-1
    #    for i in range(length):
    #        print("2 Insert:", (pos1[0]-i+1,pos1[1]))
    #        templine.append((pos1[0]-i+1,pos1[1]))
    if pos2[1] - pos1[1] > 1:
        length = pos2[1] - pos1[1]-1 
        for i in range(length):
            print("3 Insert:", (pos1[0],pos1[1]+i+1))
            templine.append((pos1[0],pos1[1]+i+1))
    #if pos1[1] - pos2[1] > 1:
    #    length = pos1[1] - pos2[1]-1
    #    for i in range(length):
    #        print("4 Insert:", (pos1[0],pos1[1]-i+1))
    #        templine.append((pos1[0],pos1[1]-i+1))

def 

def wipe():
    screen.fill(white)
    drawLines()
    drawPoints()


            
    
points = []
Spaces = []
lines = []
templine = []
size = width, height = 1000, 1000
startGame(5)




pygame.init()


#screen = pygame.display.set_mode((width, height), RESIZABLE)
screen = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN, depth=0, display=0)
pygame.display.set_caption("Sprouts")
global background
background = pygame.Surface(screen.get_size())
background.fill(white)
screen.blit(background, (0,0))
pygame.display.update()
random.seed()

drawing = False
lastPos = None
activePoint = None

drawPoints()

while 1:
    for event in pygame.event.get():
        mousePos = pygame.mouse.get_pos()
        if event.type == QUIT:
                sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            # Check if mousePos is in points with select margin
            if pygame.mouse.get_pressed()[0]:
                for content in points:
                    if ((abs(mousePos[0] - content[0])) < 15) & ((abs(mousePos[1] - content[1])) < 15):
                        print(content, " selected")
                        activePoint = content
                        drawing = True
                        lastPos = mousePos
                        lines.append([])
            if pygame.mouse.get_pressed()[2] and drawing:
                drawing = False
                lastPos = None
                activePoint = None
                wipe()
                print("update")

        # Draw freehand from active point
        elif drawing:
            drawing = checkCollision()
            if lastPos != mousePos:
                pygame.draw.line(screen, black, lastPos, mousePos, 5)
                fillBlank(lastPos,mousePos)
                appendPos(templine, mousePos)
            lastPos = mousePos
            # Check if mousePos is in points with select margin
            for content in points:
                if content == activePoint:
                    print(mousePos)
                elif ((abs(mousePos[0] - content[0])) < 15) & ((abs(mousePos[1] - content[1])) < 15):
                    drawing = False
                    lastPos = None
                    activePoint = None
                    wipe()
                    print(content, "selected")
                    lines.append(templine)
                    mid = int(len(templine)/2)
                    makePoint(int(templine[mid][0]),int(templine[mid][1]))
                    templine = []
            if not drawing:
                lastPos = None
                templine = []
                wipe()

    pygame.display.update()