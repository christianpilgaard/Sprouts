import sys, pygame, time, random, math
import numpy as np
from pygame.locals import *
pygame.init()

# COLORS #
black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255
gray = 150,150,150

# FONT & LABELS #
font = pygame.font.SysFont("monospace", 42)
restart_label = font.render("RESTART", 1, black)

# PLAYER INFO #
#Player 1
player1_color = blue
player1_label = font.render("PLAYER 1", 1, player1_color)
#Player 2
player2_color = red
player2_label = font.render("PLAYER 2", 1, player2_color)
#Current player
current_player_color = player1_color
current_player = (1,0)

# SCREEN #
size = width, height = 1920, 1080
#screen = pygame.display.set_mode((width, height), RESIZABLE)
screen = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN, depth=0, display=0)
pygame.display.set_caption("Sprouts")
global background
background = pygame.Surface(screen.get_size())
background.fill(white)
screen.blit(background, (0,0))
pygame.display.flip()
random.seed()

# POINTS & LINES #
points = [] #[0] is x, [1] is y
lines = []
point1 = (0,0)
point2 = (0,0)

# DEFINITIONS #

def add_points(left,top):
    ball = (left,top)
    points.append(ball)

def start_points(amount):
    for x in range(amount):
        add_points(random.randint(100,width-100),random.randint(100,height-100))

def draw_points():
    for x in points:
        pygame.draw.circle(screen, black, (x[0],x[1]), 25)

def draw_lines():
    for x in lines:
        pygame.draw.line(screen,x[2],x[0],x[1],15)

def point_clicked(pos):
    pygame.draw.circle(screen, current_player_color,pos,20)
    dragable = pygame.draw.line(screen, current_player_color,pos,pygame.mouse.get_pos(),15)
    if pygame.mouse.get_pressed()[2]:
        return (0,0)
    else:
        return pos

def check_collision():
    for x in points:
        ball = pygame.draw.circle(screen, black, (x[0],x[1]), 25)
        if ball.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.circle(screen, current_player_color,(x[0],x[1]),20)
            if pygame.mouse.get_pressed()[0]:
                if point1 == (0,0):
                    print("point got clicked")
                    time.sleep(.200)
                    return x
                else:
                    point2 = x
                    if point1 == point2:
                        print("you clicked the same point")
                        time.sleep(.200)
                        return (0,0)
                    else:
                        add_new_line_point(point1,point2,current_player_color)
                        print("you clicked a new point")
                        time.sleep(.200)
                        return (0,0)
    return point1

def add_new_line_point(pos1,pos2,color):
    points.append((int((pos1[0]+pos2[0])/2),int((pos1[1]+pos2[1])/2)))
    lines.append(((pos1),(pos2),color))

def change_current_player(player):
    if player[0]:
        return (0,1)
    elif player[1]:
        return (1,0)

def restart_game():
    time.sleep(1)
    screen.fill(white)
    points.clear()
    lines.clear()
    start_points(2)

# START GAME WITH N POINTS #
start_points(2)

loop = 1
while loop:
        # EVENTS #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_LSHIFT:
                    if current_player[0]:
                        current_player = (0,1)
                        current_player_color = player2_color
                    elif current_player[1]:
                        current_player = (1,0)
                        current_player_color = player1_color
                    time.sleep(.200)

        screen.fill(white)

        if current_player[0]:
            player1_label = font.render("PLAYER 1", 1, current_player_color)
            player2_label = font.render("PLAYER 2", 1, gray)
        elif current_player[1]:
            player1_label = font.render("PLAYER 1", 1, gray)
            player2_label = font.render("PLAYER 2", 1, current_player_color)

        draw_points()
        draw_lines()
        point1 = check_collision()

        if point1 != (0,0):
            point1 = point_clicked(point1)

        if point2 != (0,0):
            current_player = change_current_player()

        screen.blit(player1_label, (0,0))
        screen.blit(player2_label, (200,0))
        screen.blit(restart_label, (1500,0))

        pygame.display.flip()
