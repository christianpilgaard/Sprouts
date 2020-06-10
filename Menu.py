import pygame, sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import Sprouts

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Sprouts')
screen = pygame.display.set_mode((800,800), 0, 32)

font_h = pygame.font.SysFont(None, 100)
font_n = pygame.font.SysFont(None, 20)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    click = False
    hold = False
    circle_rect = (190, 175)
    circle_center = (200, 180)
    slider_text = 200
    slide_hold = False
    slider_no = '2'
    while True:

        screen.fill((255,255,255))
        draw_text('Main Menu', font_h, (0,0,0), screen, 400, 90)

        mx, my = pygame.mouse.get_pos()

        # Create objects
        slider_base = pygame.Rect(200, 175, 500, 10)
        slider_circle = pygame.Rect(circle_rect, (20, 20))
        button_1 = pygame.Rect(150, 235, 500, 100)
        button_2 = pygame.Rect(150, 370, 500, 100)
        button_3 = pygame.Rect(150, 505, 500, 100)
        button_4 = pygame.Rect(150, 640, 500, 100)
        if button_1.collidepoint((mx,my)):
            pygame.draw.rect(screen, (0,150,0), button_1)
            if click:
                Sprouts.startGame(int(slider_no))
                pass
                # Sprouts(int(slider_no))
                # Start simple game
        else:
            pygame.draw.rect(screen, (0,0,0), button_1)
        if button_2.collidepoint((mx,my)):
            pygame.draw.rect(screen, (0,150,0), button_2)
            if click:
                pass
                # Sprouts_Tri(int(slider_no))
                # Start advanced game
        else:
            pygame.draw.rect(screen, (0,0,0), button_2)
        if button_3.collidepoint((mx,my)):
            pygame.draw.rect(screen, (0,150,0), button_3)
            if click:
                pass
                # Start AI game
        else:
            pygame.draw.rect(screen, (0,0,0), button_3)
        if button_4.collidepoint((mx,my)):
            pygame.draw.rect(screen, (0,150,0), button_4)
            if click:
                getFile()
        else:
            pygame.draw.rect(screen, (0,0,0), button_4)
        if slider_circle.collidepoint((mx,my)):
            if hold:
                slide_hold = True
        if slide_hold:
            if mx<200:
                circle_rect = (200-10, 175)
                circle_center = (200, 180)
                slider_text = 200
                slider_no = '2'
            elif mx>700:
                circle_rect = (700-10, 175)
                circle_center = (700, 180)
                slider_text = 700
                slider_no = '20'
            elif mx>=200 and mx<=700:
                circle_rect = (mx-10, 175)
                circle_center = (mx, 180)
                slider_text = mx
                slider_no = str(int(round((mx - 200) / 27.78))+2)




        # Draw objects
        pygame.draw.rect(screen, (0,0,0), slider_base)
        pygame.draw.circle(screen, (0,150,0), circle_center, 20)
        draw_text('Sandbox', font_h, (255,255,255), screen, 400, 285)
        draw_text('Advanced', font_h, (255,255,255), screen, 400, 420)
        draw_text('A.I.', font_h, (255,255,255), screen, 400, 555)
        draw_text('txt-file', font_h, (255,255,255), screen, 400, 690)
        draw_text(slider_no, font_n, (0,0,0), screen, slider_text, 150)
        draw_text('No. of nodes:', font_n, (0,0,0), screen, 120, 180)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    hold = True
            if pygame.mouse.get_pressed()[0] == 0:
                hold = False
                slide_hold = False

        pygame.display.update()
        mainClock.tick(60)

# Select a file and run it if it's a valid txt-file
def getFile():
    Tk().withdraw()
    while True:
        filename = askopenfilename()
        if filename[-4:] == '.txt' or filename == '':
            break
    try:
        with open(filename, 'r') as f:
            lines = [line.rstrip() for line in f]
            if checkValidFile(lines):
                pass # start txt-file version
            else:
                pass # Show the player some kind of error
    except:
        pass

# Checks the validity of a txt-file
def checkValidFile(text):
    for i, line in enumerate(text):
        if i == 0:
            if len(line) != 1:
                return False
            else:
                try:
                    int(line)
                except:
                    return False
        else:
            if len(line) != 3 or line[1] != ' ':
                return False
            else:
                try:
                    int(line[0])
                    int(line[2])
                except:
                    return False
    return True



main_menu()
