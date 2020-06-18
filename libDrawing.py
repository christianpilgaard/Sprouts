import pygame, random, sys, math
import numpy as np
from pygame.locals import *
from libSystem import *
from libNode import *
from libController import *

import libSystem


# -------------------------------------------------------------------
# --------------------------- MAIN GAME -----------------------------
# -------------------------------------------------------------------
class Drawing:
    def __init__(self):
        self.system = System(800, 800)
        self.controller = GameController()

    def playDrawing(self, amount):
        system = self.system
        controller = self.controller

        controller.resetGame()

        # Initialize game
        system.init()
        controller.startGame(amount)

        # Game loop -----------------------------
        while 1:
            for event in pygame.event.get():
                controller.setMousePos(pygame.mouse.get_pos())

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
                    if system.getBackButton().collidepoint(pygame.mouse.get_pos()):
                        return 0
                    elif system.getRestartButton().collidepoint(pygame.mouse.get_pos()):
                        return 1

                    for node in controller.getNodes():
                        if controller.nodeCollision(node, controller.getMousePos(), "node"):
                            if len(node.getRelations()) < 3:
                                controller.setActiveNode(node)
                                node.getRelations().append(-1)
                                controller.setDrawing(True)
                                controller.setLastPos(controller.getMousePos())

                # Draw from node ---------------------------
                if controller.getDrawing():
                    controller.setDrawing(controller.checkCollision())
                    if controller.getLastPos() is not None:
                        if controller.getLastPos() != controller.getMousePos():
                            print(controller.getMousePos())
                            system.updatePath(controller.getLastPos(), controller.getMousePos())
                            controller.fillBlank(controller.getLastPos(), controller.getMousePos())
                            controller.getTempEdge().append(controller.getMousePos())
                    controller.setLastPos(controller.getMousePos())

                    # Check if any node or line is hit -----------------------------
                    # Avoid initially targeting active point
                    if not controller.getMoved():
                        if controller.reverseNodeCollision(controller.getActiveNode(), controller.getMousePos()):
                            controller.setMoved(True)

                    else:
                        # Check for hit detection while drawing
                        for i, node in enumerate(controller.getNodes()):
                            if controller.nodeCollision(node, controller.getMousePos(), "node"):
                                if len(node.getRelations()) < 3:
                                    # Append an edge connecting the nodes
                                    # Add new node on edge

                                    if controller.checkEdge(controller.getTempEdge()):
                                        controller.getEdges().append(controller.getTempEdge())
                                        mid = int(len(controller.getTempEdge()) / 2)
                                        controller.addNode(int(controller.getTempEdge()[mid][0]), int(controller.getTempEdge()[mid][1]))
                                        controller.setTempEdge([])

                                        # Remove placeholder relation
                                        controller.getActiveNode().getRelations().remove(-1)

                                        # Add relations between connected nodes
                                        controller.getActiveNode().getRelations().append(controller.getNodes()[-1].getId())
                                        controller.getNodes().__getitem__(node.getId()).getRelations().append(controller.getNodes()[-1].getId())
                                        controller.getNodes().__getitem__(-1).getRelations().append(controller.getActiveNode())
                                        controller.getNodes().__getitem__(-1).getRelations().append(node.getId())
                                        controller.setActiveNode(None)
                                        controller.setOverlap(False)

                                        # Change turn
                                        controller.setTurn(controller.getTurn() + 1)

                                # Reset current drawing
                                controller.setLastPos(None)
                                controller.setMoved(False)
                                controller.setDrawing(False)

                                # Remove placeholder relation
                                controller.removePlaceholder()

                                # Update screen
                                system.updateScreen1(True, controller.getNodes(), controller.getEdges(), controller.getSize(), 5, controller.getPlayer())

                    if not controller.getDrawing():
                        # Reset current drawing
                        controller.setLastPos(None)
                        controller.setMoved(False)
                        controller.setDrawing(False)
                        controller.setTempEdge([])

                        # Remove placeholder relation
                        controller.removePlaceholder()

                        # Update screen
                        system.updateScreen1(True, controller.getNodes(), controller.getEdges(), controller.getSize(), 5, controller.getPlayer())

            system.updateScreen1(False, controller.getNodes(), controller.getEdges(), controller.getSize(), 5, controller.getPlayer())
            pygame.display.update()
