import pygame, random, sys, math
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
            for inp in txt_input:
                s = controller.findNode(int(inp[0]) - 1)
                e = controller.findNode(int(inp[2]) - 1)

                if len(s.getRelations()) < 3 and len(e.getRelations()) < 3:
                    paths = pathfinding(TriangulationLogic.getDt(), s.getPos(), e.getPos()).paths

                    if len(paths) > 0:
                        print("more moves")
                        i = random.randint(0, len(paths) - 1)

                        for j, point in enumerate(paths[i]):
                            if not j == 0:
                                controller.getEdges().append([paths[i][j - 1], point])
                                if not point == paths[i][-1]:
                                    triLogic.getChosenCenter().append(point)

                        if len(triLogic.getChosenCenter()) > 0:
                            mid = triLogic.getChosenCenter()[int(len(triLogic.getChosenCenter()) / 2)]
                        else:
                            mid = [(s.getX() + e.getX()) / 2,
                                   (s.getY() + e.getY()) / 2]
                        controller.addNode(mid[0], mid[1])

                        # Add relations between connected nodes
                        s.getRelations().append(e.getId())
                        e.getRelations().append(s.getId())

                        # Add new path and node
                        triLogic.getDt().addPath(s.getPos(), e.getPos(), triLogic.getChosenCenter(), mid)
                        triLogic.updateCentroids(triLogic.getCentroids(), triLogic.getCentersize())
                        triLogic.clearChosenCenter()

                        controller.setTurn(controller.getTurn() + 1)

                        system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(),
                                             triLogic.getDt().allEdges,
                                             triLogic.getNeighbours(), controller.getSize(), triLogic.getCentersize(), 5,
                                             controller.getPlayer())
                        pygame.display.update()

                    else:
                        controller.setError(True)
                        break

                time.sleep(2.0)

            while controller.getError():
                view.updateScreen()
                close = view.drawPopUp('Unable to make the move.')
                pygame.display.update()
                if close:
                    return 0

            while 1:
                view.updateScreen()
                close = view.drawPopUp('No more moves in file.')
                pygame.display.update()
                if close:
                    return 0

        # Game loop -----------------------------
        while 1:
            if controller.getDone():
                system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(), triLogic.getDt().allEdges,
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
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return 0
                    elif event.key == K_BACKSPACE:
                        return 2

                # Mouse action -----------------------------
                elif event.type == MOUSEBUTTONDOWN:

                    # Check if the buttons are pressed ------
                    if system.back_button.collidepoint(pygame.mouse.get_pos()):
                        return 0
                    elif system.restart_button.collidepoint(pygame.mouse.get_pos()):
                        return 2

                    # No active node ------------------------
                    if controller.getActivePos() is None:
                        for node in controller.getNodes():
                            if controller.nodeCollision(node, mousePos, "node"):
                                if len(node.getRelations()) < 3:
                                    controller.setActiveNode(node)
                                    controller.setActivePos(controller.getActiveNode().getPos())
                                    node.getRelations().append(-1)
                                    triLogic.setNeighbours(triLogic.getDt().exportNeighbours(node.getPos(), "node", triLogic.getChosenCenter(), controller.getActiveNode().getPos()))

                    # Active node ---------------------------
                    if controller.getActivePos() is not None:

                        # Select centroid -------------------
                        for centerNode in triLogic.getCentroids():
                            if centerNode in triLogic.getNeighbours():
                                if controller.nodeCollision(centerNode, mousePos, "centerNode"):
                                    controller.getEdges().append([controller.getActivePos(), centerNode])
                                    controller.setActivePos(centerNode)
                                    triLogic.getChosenCenter().append(centerNode)

                                    triLogic.getNeighbours().clear()
                                    triLogic.setNeighbours(triLogic.getDt().exportNeighbours(centerNode,
                                            "centerNode", triLogic.getChosenCenter(), controller.getActiveNode().getPos()))

                        # Select end node ------------------
                        for node in controller.getNodes():
                            if controller.nodeCollision(node, mousePos, "node"):
                                if [node.getX(), node.getY()] in triLogic.getNeighbours():
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
                                        controller.getNodes().__getitem__(node.getId()).getRelations().append(controller.getNodes()[-1].getId())
                                        controller.getNodes().__getitem__(-1).getRelations().append(controller.getActiveNode())
                                        controller.getNodes().__getitem__(-1).getRelations().append(node.getId())

                                        # Add new path and node
                                        triLogic.getDt().addPath(controller.getActiveNode().getPos(), node.getPos(), triLogic.getChosenCenter(), mid)
                                        triLogic.updateCentroids()
                                        triLogic.clearChosenCenter()
                                        triLogic.clearNeighbours()

                                        controller.setActiveNode(None)
                                        controller.setActivePos(None)

                                    # Remove placeholder relation
                                    controller.removePlaceholder()

                                    # win detection
                                    if controller.getTurn() == 3 * amount - 1:
                                        print("True")
                                        controller.setDone(True)
                                    elif controller.getTurn() >= 2 * amount:
                                        unlockedNodes = []
                                        Check = True
                                        controller.setDone(False)
                                        for node in controller.getNodes():
                                            if len(node.getRelations()) < 2:
                                                Check = False
                                                break
                                            elif len(node.getRelations()) < 3:
                                                unlockedNodes.append(node)
                                        if Check:
                                            for i, uNode in enumerate(unlockedNodes):
                                                if not i == 0:
                                                    paths = pathfinding(TriangulationLogic.getDt(),
                                                                        unlockedNodes[i - 1].getPos(),
                                                                        uNode.getPos()).paths
                                                    if len(paths) > 0:
                                                        controller.setDone(False)
                                                        break
                                                    elif i == len(unlockedNodes) - 1:
                                                        controller.setDone(True)

            system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.getCentroids(), triLogic.getDt().allEdges,
                                 triLogic.getNeighbours(), controller.getSize(), triLogic.getCentersize(), 5, controller.getPlayer())
            pygame.display.update()
