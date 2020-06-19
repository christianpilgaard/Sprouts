import pygame, sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pygame.locals import *

from libSystem import *
from libController import *
from libDrawing import *
from libAdvanced import *

class Menu:
    def __init__(self):
        self.system = System(800, 800)
        self.controller = GameController()

    def showMenu(self):
        system = self.system
        controller = self.controller
        screen = system.getScreen()
        fontBig = system.getFontBig()
        fontSmall = system.getFontSmall()

        black = system.getBlack()
        white = system.getWhite()
        green = system.getDGreen()

        click = False
        hold = False
        slider_text = 200
        slide_hold = False
        slider_no = '2'
        error_text = ''
        # Create objects
        circle_rect = (190, 175)
        circle_center = (200, 180)
        slider_base = pygame.Rect(200, 175, 500, 10)
        button_1 = pygame.Rect(150, 235, 500, 100)
        button_2 = pygame.Rect(150, 370, 500, 100)
        button_3 = pygame.Rect(150, 505, 500, 100)
        button_4 = pygame.Rect(150, 640, 500, 100)
        while True:
            system.getScreen().fill(white)
            system.drawText('Sprouts', fontBig, black, screen, 400, 90)

            slider_circle = pygame.Rect(circle_rect, (20, 20))

            mx, my = pygame.mouse.get_pos()

            if button_1.collidepoint((mx,my)) and error_text == '':
                pygame.draw.rect(screen, green, button_1)
                if click:
                    play = 1
                    while play:
                        play = Drawing().playDrawing(int(slider_no))
            else:
                pygame.draw.rect(screen, black, button_1)
            if button_2.collidepoint((mx,my)) and error_text == '':
                pygame.draw.rect(screen, green, button_2)
                if click:
                    play = 1
                    while play:
                        play = Advanced().playAdvanced(int(slider_no), False, [])
            else:
                pygame.draw.rect(screen, black, button_2)
            if button_3.collidepoint((mx,my)) and error_text == '':
                pygame.draw.rect(screen, green, button_3)
                if click:
                    pass
            else:
                pygame.draw.rect(screen, black, button_3)
            if button_4.collidepoint((mx,my)) and error_text == '':
                pygame.draw.rect(screen, green, button_4)
                if click:
                    error_text = self.getFile()
            else:
                pygame.draw.rect(screen, black, button_4)
            if slider_circle.collidepoint((mx,my)) and error_text == '':
                if hold:
                    slide_hold = True
            if (slide_hold or (slider_base.collidepoint((mx,my)) and click)) and error_text == '':
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
            pygame.draw.rect(screen, black, slider_base)
            pygame.draw.circle(screen, green, circle_center, 20)
            system.drawText('Drawing', fontBig, white, screen, 400, 285)
            system.drawText('Advanced', fontBig, white, screen, 400, 420)
            system.drawText('A.I.', fontBig, white, screen, 400, 555)
            system.drawText('txt-file', fontBig, white, screen, 400, 690)
            system.drawText(slider_no, fontSmall, black, screen, slider_text, 150)
            system.drawText('No. of nodes:', fontSmall, black, screen, 120, 180)

            if not error_text == '':
                error_frame = pygame.Rect(195, 295, 410, 210)
                error = pygame.Rect(200, 300, 400, 200)
                error_button = pygame.Rect(350, 425, 100, 50)
                pygame.draw.rect(screen, (0,0,0), error_frame)
                pygame.draw.rect(screen, (255,255,255), error)
                if error_button.collidepoint((mx,my)):
                    pygame.draw.rect(screen, (0,150,0), error_button)
                    if click:
                        error_text = ''
                else:
                    pygame.draw.rect(screen, (0,0,0), error_button)
                system.drawText(error_text, fontSmall, (0,0,0), screen, 400, 350)
                system.drawText('Close', fontSmall, (255,255,255), screen, 400, 450)

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
            system.getMainClock().tick(60)

    # Select a file and run it if it's a valid txt-file
    def getFile(self):
        Tk().withdraw()
        filename = askopenfilename()
        if filename == '':
            return ''
        elif filename[-4:] != '.txt':
            return 'Expected a txt-file.'
        try:
            with open(filename, 'r') as f:
                lines = [line.rstrip() for line in f]
                if self.checkValidFile(lines):
                    play = 1
                    while play:
                        play = Advanced().playAdvanced(int(lines[0]), True, lines[1:]) # start txt-file version
                else:
                    return 'Unexpected file content format.'
        except:
            pass
        return ''

    # Checks the validity of a txt-file
    def checkValidFile(self, text):
        for i, line in enumerate(text):
            if i == 0:
                try:
                    int(line)
                except:
                    return False
            else:
                if ' ' not in line[1:-1]:
                    return False
                else:
                    try:
                        int(line[:line.find(' ')])
                        int(line[line.find(' '):])
                    except:
                        return False
        return True
