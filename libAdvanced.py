import pygame, random, sys, math, time
import numpy as np
from pygame.locals import *
from Triangulation import Triangulation
from BFS import pathfinding
from libSystem import *
from libNode import *
from libController import *
from libTriangulationLogic import *


# -------------------------------------------------------------------
# --------------------------- MAIN GAME -----------------------------
# -------------------------------------------------------------------
class Advanced:
    def __init__(self):
        self.system = System(800, 800)
        self.controller = GameController()
        self.triLogic = TriangulationLogic()

    def playAdvanced(self, amount, txt, txt_input):
        system = self.system
        controller = self.controller
        triLogic = self.triLogic

        controller.resetGame()
        triLogic.resetGame()
        # Initialize game
        system.init()
        controller.startGame(amount)
        triLogic.initializeTriangulation(controller.getNodes())
        if txt:
            system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(),
                                 triLogic.dt.getAllEdges(),
                                 triLogic.getNeighbours(), controller.getSize(), triLogic.getCentersize(), 5,
                                 controller.getPlayer())
            pygame.display.update()
            for inp in txt_input:
                s = controller.findNode(int(inp[:inp.find(' ')]) - 1)
                e = controller.findNode(int(inp[inp.find(' '):]) - 1)

                if len(s.getRelations()) < 3 and len(e.getRelations()) < 3:
                    paths = pathfinding(triLogic.dt, s.getPos(), e.getPos()).getPaths()

                    if len(paths) > 0:
                        i = random.randint(0, len(paths) - 1)

                        for j, point in enumerate(paths[i]):
                            if not j == 0:
                                controller.getEdges().append([paths[i][j - 1], point])
                                if not point == paths[i][-1]:
                                    triLogic.getChosenCenter().append(point)


                        if len(triLogic.getChosenCenter()) > 0:
                            mid = triLogic.getChosenCenter()[int(len(triLogic.getChosenCenter()) / 2)]
                        else:
                            mid = [(s.getX() + e.getX()) / 2, (s.getY() + e.getY()) / 2]
                        controller.addNode(mid[0], mid[1])


                        # Add relations between connected nodes
                        s.getRelations().append(e)
                        e.getRelations().append(s)


                        # Add new path and node
                        triLogic.dt.addPath(s.getPos(), e.getPos(), triLogic.getChosenCenter(), mid)
                        triLogic.updateCentroids() # Går tilbage til menu her
                        triLogic.clearChosenCenter()

                        controller.setTurn(controller.getTurn() + 1)

                        system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(),
                                             triLogic.dt.getAllEdges(),
                                             triLogic.getNeighbours(), controller.getSize(), triLogic.getCentersize(), 5,
                                             controller.getPlayer())
                        pygame.display.update()
                    else:
                        controller.setError(True)
                        break
                startTime = time.time()
                while 3 > time.time() - startTime:
                    for event in pygame.event.get():
                        mousePos = pygame.mouse.get_pos()

                        # Quit game
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                return 0
                            elif event.key == K_BACKSPACE:
                                return 1

                        # Mouse action -----------------------------
                        elif event.type == MOUSEBUTTONDOWN:

                            # Check if the buttons are pressed ------
                            if system.getBackButton().collidepoint(pygame.mouse.get_pos()):
                                return 0
                            elif system.getRestartButton().collidepoint(pygame.mouse.get_pos()):
                                return 1

            if controller.getError():
                while 1:
                    close = system.drawPopUp('Unable to make the move.')
                    pygame.display.update()
                    if close:
                        break
            else:
                while 1:
                    close = system.drawPopUp('No more moves in file.')
                    pygame.display.update()
                    if close:
                        break
            while 1:
                system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(),
                                     triLogic.dt.getAllEdges(),
                                     triLogic.getNeighbours(), controller.getSize(), triLogic.getCentersize(), 5,
                                     controller.getPlayer())
                pygame.display.update()
                for event in pygame.event.get():
                    mousePos = pygame.mouse.get_pos()

                    # Quit game
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return 0
                        elif event.key == K_BACKSPACE:
                            return 1

                    # Mouse action -----------------------------
                    elif event.type == MOUSEBUTTONDOWN:

                        # Check if the buttons are pressed ------
                        if system.getBackButton().collidepoint(pygame.mouse.get_pos()):
                            return 0
                        elif system.getRestartButton().collidepoint(pygame.mouse.get_pos()):
                            return 1

        # Game loop -----------------------------
        while 1:
            while controller.getDone():
                system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(), triLogic.dt.getAllEdges(),
                                     triLogic.getNeighbours(), controller.getSize(), triLogic.getCentersize(), 5,
                                     controller.getPlayer())
                close = system.displayWinner(controller.getPlayer())
                pygame.display.update()
                if close:
                    return 0

            for event in pygame.event.get():
                mousePos = pygame.mouse.get_pos()

                # Quit game
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return 0
                    elif event.key == K_BACKSPACE:
                        return 1

                # Mouse action -----------------------------
                elif event.type == MOUSEBUTTONDOWN:

                    # Check if the buttons are pressed ------
                    if system.getBackButton().collidepoint(pygame.mouse.get_pos()):
                        return 0
                    elif system.getRestartButton().collidepoint(pygame.mouse.get_pos()):
                        return 1

                    # No active node ------------------------
                    if controller.getActivePos() is None:
                        for node in controller.getNodes():
                            if controller.nodeCollision(node, mousePos, "node"):
                                if len(node.getRelations()) < 3:
                                    controller.setActiveNode(node)
                                    controller.setActivePos(controller.getActiveNode().getPos())
                                    node.getRelations().append(-1)
                                    triLogic.setNeighbours(triLogic.dt.exportNeighbours(node.getPos(), "node", triLogic.getChosenCenter(), controller.getActiveNode().getPos()))

                    # Active node ---------------------------
                    if controller.getActivePos() is not None:

                        # Select centroid -------------------
                        for centerNode in triLogic.getCentroids():
                            if centerNode in triLogic.getNeighbours():
                                if controller.nodeCollision(centerNode, mousePos, "centerNode"):
                                    triLogic.getChosenCenter().append(centerNode)

                                    triLogic.getNeighbours().clear()
                                    triLogic.setNeighbours(triLogic.dt.exportNeighbours(centerNode, "centerNode", triLogic.getChosenCenter(), controller.getActiveNode().getPos()))



                                    if len(triLogic.getNeighbours()) > 0:
                                        controller.getEdges().append([controller.getActivePos(), centerNode])
                                        controller.getTempEdge().append([controller.getActivePos(), centerNode])
                                        controller.setActivePos(centerNode)
                                    else:
                                        for edge in controller.getTempEdge():
                                            controller.getEdges().remove(edge)
                                        controller.getActiveNode().getRelations().remove(-1)
                                        triLogic.updateCentroids()
                                        triLogic.clearChosenCenter()
                                        triLogic.clearNeighbours()
                                        controller.getTempEdge().clear()
                                        controller.setActiveNode(None)
                                        controller.setActivePos(None)

                        # Select end node ------------------
                        for node in controller.getNodes():
                            if controller.nodeCollision(node, mousePos, "node"):
                                if node.getPos() in triLogic.getNeighbours():
                                    if len(node.getRelations()) < 3:
                                        controller.getEdges().append([controller.getActivePos(), node.getPos()])

                                        if len(triLogic.getChosenCenter()) > 0:
                                            mid = triLogic.getChosenCenter()[int(len(triLogic.getChosenCenter()) / 2)]
                                        else:
                                            mid = [(controller.getActivePos()[0] + mousePos[0]) / 2, (controller.getActivePos()[1] + mousePos[1]) / 2]
                                        controller.addNode(mid[0], mid[1])

                                        # Remove placeholder relation
                                        controller.getActiveNode().getRelations().remove(-1)

                                        # Add relations between connected nodes
                                        controller.getActiveNode().getRelations().append(controller.getNodes()[-1].getId())
                                        controller.getNodes().__getitem__(node.getId()).getRelations().append(controller.getNodes()[-1])
                                        controller.getNodes().__getitem__(-1).getRelations().append(controller.getActiveNode())
                                        controller.getNodes().__getitem__(-1).getRelations().append(node)

                                        # Add new path and node
                                        triLogic.dt.addPath(controller.getActiveNode().getPos(), node.getPos(), triLogic.getChosenCenter(), mid)
                                        triLogic.updateCentroids()
                                        triLogic.clearChosenCenter()
                                        triLogic.clearNeighbours()

                                        controller.getTempEdge().clear()
                                        controller.setActiveNode(None)
                                        controller.setActivePos(None)

                                        controller.setTurn(controller.getTurn() + 1)

                                    # Remove placeholder relation
                                    controller.removePlaceholder()

                                    # win detection
                                    if controller.getTurn() == 3 * amount - 1:
                                        controller.setDone(True)
                                    elif controller.getTurn() >= 2 * amount:
                                        unlockedNodes = []
                                        Check = True
                                        controller.setDone(True)
                                        for node in controller.getNodes():
                                            if len(node.getRelations()) < 2:
                                                Check = False
                                                break
                                            elif len(node.getRelations()) < 3:
                                                unlockedNodes.append(node)
                                        if Check:
                                            for i, uNode1 in enumerate(unlockedNodes):
                                                for uNode2 in unlockedNodes[i+1:]:
                                                    paths = pathfinding(triLogic.dt, uNode1.getPos(), uNode2.getPos()).getPaths()
                                                    if len(paths) > 0:
                                                        controller.setDone(False)
                                                        break
                                                if not controller.getDone():
                                                    break
                                                elif i == len(unlockedNodes) - 1:
                                                    controller.setDone(True)

            system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(), triLogic.dt.getAllEdges(),
                                 triLogic.getNeighbours(), controller.getSize(), triLogic.getCentersize(), 5, controller.getPlayer())
            pygame.display.update()
