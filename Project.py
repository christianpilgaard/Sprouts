import pygame, random, sys
from pygame.locals import *

black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255
gray = 150,150,150


def makePoint (x, y, r):
    point = (int(x), int(y), r)
    points.append(point)

def startGame (p):
    points.clear()
    if p == 2:
        makePoint(1*width/3,1*height/2, 0)
        makePoint(2*width/3,1*height/2, 0)
    rand = random.randint(0,1)
    if p == 3:
        rand = random.randint(0,1)
        if rand > 0.5:
            makePoint(1*width/2,1*height/3, 0)
            makePoint(2*width/3,2*height/3, 0)
            makePoint(1*width/3,2*height/3, 0)
        else:
            makePoint(1*width/4,1*height/2, 0)
            makePoint(2*width/4,1*height/2, 0)
            makePoint(3*width/4,1*height/2, 0)
    elif p == 4:
        if rand > 0.5:
            makePoint(2*width/5,2*height/5, 0)
            makePoint(4*width/5,2*height/5, 0)
            makePoint(2*width/5,4*height/5, 0)
            makePoint(4*width/5,4*height/5, 0)
        else:
            makePoint(2*width/9,2*height/5, 0)
            makePoint(6*width/9,2*height/5, 0)
            makePoint(4*width/9,4*height/5, 0)
            makePoint(8*width/9,4*height/5, 0)
    elif p == 5:
        if rand > 0.5:
            makePoint(2*width/5,2*height/5, 0)
            makePoint(4*width/5,2*height/5, 0)
            makePoint(2*width/5,4*height/5, 0)
            makePoint(4*width/5,4*height/5, 0)
            makePoint(3*width/5,3*height/5, 0)
        else:
            makePoint(4*width/7,2*height/7, 0)
            makePoint(2*width/7,3*height/7, 0)
            makePoint(6*width/7,3*height/7, 0)
            makePoint(3*width/7,5*height/7, 0)
            makePoint(5*width/7,5*height/7, 0)

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
    # ADD TO X AND ADD TO Y
    new_posX = ()
    new_posY = ()
    new_pos = ()
    print(pos1)
    print(pos2)
    if pos2[0] - pos1[0] > 1 and pos2[1] - pos1[1] > 1:
        new_posX = (pos1[0]+1,pos1[1])
        new_posY = (pos1[0],pos1[1]+1)
        new_pos = (pos1[0]+1,pos1[1]+1)

    # ADD TO X AND SUBTRACT FROM Y
    elif pos2[0] - pos1[0] > 1 and pos1[1] - pos2[1] > 1:
        new_posX = (pos1[0]+1,pos1[1])
        new_posY = (pos1[0],pos1[1]-1)
        new_pos = (pos1[0]+1,pos1[1]-1)
    # SUBTRACT FROM X AND ADD TO Y
    elif pos1[0] - pos2[0] > 1 and pos2[1] - pos1[1] > 1:
        new_posX = (pos1[0]-1,pos1[1])
        new_posY = (pos1[0],pos1[1]+1)
        new_pos = (pos1[0]-1,pos1[1]+1)
    # SUBTRACT FROM X AND SUBTRACT FROM Y
    elif pos1[0] - pos2[0] > 1 and pos1[1] - pos2[1] > 1:
        new_posX = (pos1[0]-1,pos1[1])
        new_posY = (pos1[0],pos1[1]-1)
        new_pos = (pos1[0]-1,pos1[1]-1)
    # ADD TO X
    elif pos2[0] - pos1[0] > 1:
        new_posX = (pos1[0]+1,pos1[1])
        new_pos = new_posX
    # SUBTRACT FROM X
    elif pos1[0] - pos2[0] > 1:
        new_posX = (pos1[0]-1,pos1[1])
        new_pos = new_posX
    # ADD TO Y
    elif pos2[1] - pos1[1] > 1:
        new_posY = (pos1[0],pos1[1]+1)
        new_pos = new_posY
    # SUBTRACT FROM Y
    elif pos1[1] - pos2[1] > 1:
        new_posY = (pos1[0],pos1[1]-1)
        new_pos = new_posY

    if new_posX != ():
        templine.append(new_posX)
    if new_posY != ():
        templine.append(new_posY)

    if new_pos != pos2 and new_pos != ():
        fillBlank(new_pos, pos2)


def wipe(t):
    screen.fill(white)
    if t == 1:
        text = font.render('1st player', True, green, blue)
    else:
        text = font.render('2nd player', True, green, blue)
    screen.blit(text, textRect)
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
textRect.center = (1000, 200)

screen.blit(background, (0,0))
screen.blit(text, textRect)
pygame.display.update()
random.seed()

drawing = False
lastPos = None
activePoint = None
activeItem = None
turn = 1

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
                for i, content in enumerate(points):
                    if ((abs(mousePos[0] - content[0])) < 15) & ((abs(mousePos[1] - content[1])) < 15) & (content[2] < 3):
                        print(content, " selected")
                        activePoint = content
                        activeItem = i
                        drawing = True
                        lastPos = mousePos
                        lines.append([])
            if pygame.mouse.get_pressed()[2] and drawing:
                drawing = False
                lastPos = None
                activePoint = None
                activeItem = None
                wipe(turn)
                print("update")

        # Draw freehand from active point
        elif drawing:
            drawing = checkCollision()
            if lastPos != mousePos:
                pygame.draw.line(screen, black, lastPos, mousePos, 5)
                fillBlank(lastPos, mousePos)
                appendPos(templine, mousePos)
            lastPos = mousePos
            # Check if mousePos is in points with select margin
            for i, content in enumerate(points):
                if content == activePoint:
                    print(mousePos)
                elif ((abs(mousePos[0] - content[0])) < 15) & ((abs(mousePos[1] - content[1])) < 15) & (content[2] < 3):
                    drawing = False
                    lastPos = None
                    # Add 1 to the references in the two connected points
                    points[i] = (int(content[0]), int(content[1]), int(content[2] + 1))
                    points[activeItem] = (activePoint[0], activePoint[1], (activePoint[2] + 1))
                    activePoint = None
                    activeItem = None
                    if turn == 1:
                        turn = 2
                    else:
                        turn = 1
                    wipe(turn)
                    print(content, "selected")
                    lines.append(templine)
                    mid = int(len(templine)/2)
                    makePoint(int(templine[mid][0]), int(templine[mid][1]), 2)
                    templine = []
                elif ((abs(mousePos[0] - content[0])) < 15) & ((abs(mousePos[1] - content[1])) < 15) & (content[2] >= 3):
                    drawing = False
                    lastPos = None
                    activePoint = None
                    activeItem = None
                    screen.fill(white)
            if not drawing:
                lastPos = None
                templine = []
                wipe(turn)

    pygame.display.update()