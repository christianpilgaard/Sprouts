import pygame, random, sys, math
import numpy as np
from pygame.locals import *
from libSystem import *
from libNode import *
from libController import *


# -------------------------------------------------------------------
# --------------------------- MAIN GAME -----------------------------
# -------------------------------------------------------------------
def playGame(amount):
    controller.resetGame()

    # Initialize game
    system.init()
    controller.startGame(amount)
    controller.drawing = False

    # Game loop -----------------------------
    while 1:
        for event in pygame.event.get():
            controller.mousePos = pygame.mouse.get_pos()

            # Quit game
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_BACKSPACE:
                    return
                elif event.key == K_SPACE:
                    print("Space")

            # Select node -----------------------------
            # Mouse 1 for drawing
            elif event.type == MOUSEBUTTONDOWN:
                if system.back_button.collidepoint(pygame.mouse.get_pos()):
                    return 0
                elif system.restart_button.collidepoint(pygame.mouse.get_pos()):
                    return 1

                for node in controller.getNodes():
                    if controller.nodeCollision(node, controller.getMousePos(), "node"):
                        if len(node.relations) < 3:
                            controller.setActiveNode(node)
                            controller.setActiveItem(node.id)
                            controller.setActivePos([controller.getActiveNode().x, controller.getActiveNode().y])
                            node.relations.append(-1)
                            controller.drawing = True
                            controller.lastPos = controller.getMousePos()

            # Draw from node ---------------------------
            if controller.getDrawing():
                controller.drawing = controller.checkCollision()
                if controller.getLastPos() is not None:
                    if controller.getLastPos() != controller.getMousePos():
                        print(controller.getMousePos())
                        system.updatePath(controller.getLastPos(), controller.getMousePos())
                        controller.fillBlank(controller.getLastPos(), controller.getMousePos())
                        controller.tempEdge.append(controller.getMousePos())
                controller.lastPos = controller.getMousePos()

                # Check if any node or line is hit -----------------------------
                # Avoid initially targeting active point
                if not controller.getMoved():
                    if controller.reverseNodeCollision(controller.getNodes().__getitem__(controller.getActiveItem()), controller.getMousePos()):
                        controller.moved = True

                else:
                    # Check for hit detection while drawing
                    for i, node in enumerate(controller.getNodes()):
                        if controller.nodeCollision(node, controller.getMousePos(), "node"):
                            if len(node.relations) < 3:
                                # Append an edge connecting the nodes
                                # Add new node on edge

                                if controller.checkEdge(controller.getTempEdge()):
                                    controller.edges.append(controller.tempEdge)
                                    mid = int(len(controller.getTempEdge()) / 2)
                                    controller.addNode(int(controller.getTempEdge()[mid][0]), int(controller.getTempEdge()[mid][1]))
                                    controller.tempEdge = []

                                    # Remove placeholder relation
                                    controller.getNodes().__getitem__(controller.getActiveItem()).relations.remove(-1)

                                    # Add relations between connected nodes
                                    controller.getNodes().__getitem__(controller.getActiveItem()).relations.append(controller.getNodes()[-1].id)
                                    controller.getNodes().__getitem__(node.id).relations.append(controller.getNodes()[-1].id)
                                    controller.getNodes().__getitem__(-1).relations.append(controller.getActiveItem())
                                    controller.getNodes().__getitem__(-1).relations.append(node.id)
                                    controller.activeNode = None
                                    controller.activeItem = None
                                    controller.overlap = False

                                    # Change turn
                                    controller.setTurn(controller.getTurn() + 1)

                            # Reset current drawing
                            controller.lastPos = None
                            controller.moved = False
                            controller.drawing = False

                            # Remove placeholder relation
                            controller.removePlaceholder()

                            # Update screen
                            system.updateScreen1(True, controller.getNodes(), controller.getEdges(), controller.size, 5, controller.getPlayer())

                if not controller.getDrawing():
                    # Reset current drawing
                    controller.lastPos = None
                    controller.moved = False
                    controller.drawing = False
                    controller.tempEdge = []

                    # Remove placeholder relation
                    controller.removePlaceholder()

                    # Update screen
                    system.updateScreen1(True, controller.getNodes(), controller.getEdges(), controller.size, 5, controller.getPlayer())

        system.updateScreen1(False, controller.getNodes(), controller.getEdges(), controller.size, 5, controller.getPlayer())
        pygame.display.update()


# ------------------------------------------------
# Initialize classes
controller = GameController()
system = System()