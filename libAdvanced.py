import pygame, random, sys, math, time
import numpy as np
from pygame.locals import *
from BFS import pathfinding
from libSystem import *
from libController import *
from libTriangulationLogic import *
from libAI import *


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

        # Initialize game
        system.init()
        controller.startGame(amount)
        triLogic.initializeTriangulation(controller.getNodes())
        if txt:
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
                        s.getRelations().append(controller.getNodes()[-1].getId())
                        e.getRelations().append(controller.getNodes()[-1])
                        controller.getNodes().__getitem__(-1).getRelations().append(s)
                        controller.getNodes().__getitem__(-1).getRelations().append(e)

                        # Add new path and node
                        triLogic.dt.addPath(s.getPos(), e.getPos(), triLogic.getChosenCenter(), mid) # Crasher her

                        minRadius = triLogic.dt.exportMinRadius()
                        if minRadius < controller.getSize():
                            controller.setSize(math.floor(minRadius))
                            triLogic.setCentersize((math.floor(minRadius * 2 / 3)))

                        triLogic.updateCentroids()
                        triLogic.clearChosenCenter()

                        controller.setTurn(controller.getTurn() + 1)

                        # Update view
                        system.fillWhite()
                        system.drawGUI()
                        system.updateEdges2(controller.getEdges(), controller.getThickness())
                        system.updateNeighbours(triLogic.getNeighbours(), 12)
                        system.updateNodes(controller.getNodes(), controller.getSize())
                        system.displayPlayer(controller.getPlayer())
                        system.drawText('%s to %s' % (inp[:inp.find(' ')], inp[inp.find(' ')+1:]), system.getFontMedium(), system.getBlack(), system.getScreen(), 600, 45)
                        pygame.display.update()
                    else:
                        controller.setError(True)
                        break
                else:
                    controller.setError(True)
                    break

                # Wait for input
                nextButton = pygame.Rect(680, 20, 100, 50)
                wait = True
                while wait:
                    pygame.draw.rect(system.getScreen(), system.getBlack(), nextButton)
                    system.drawText('next', system.getFontMedium(), system.getWhite(), system.getScreen(), 730, 45)
                    if controller.getSpace():
                        system.drawId(controller.getNodes())
                    else:
                        system.updateNodes(controller.getNodes(), controller.getSize())
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
                            elif event.key == K_SPACE:
                                controller.setSpace(not controller.getSpace())

                        # Mouse action -----------------------------
                        elif event.type == MOUSEBUTTONDOWN:

                            # Check if the buttons are pressed ------
                            if system.getBackButton().collidepoint(pygame.mouse.get_pos()):
                                return 0
                            elif system.getRestartButton().collidepoint(pygame.mouse.get_pos()):
                                return 1
                            elif nextButton.collidepoint(pygame.mouse.get_pos()):
                                wait = False

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
                system.fillWhite()
                system.drawGUI()
                system.updateEdges2(controller.getEdges(), controller.getThickness())
                system.updateNeighbours(triLogic.getNeighbours(), 12)
                system.updateNodes(controller.getNodes(), controller.getSize())
                system.displayPlayer(controller.getPlayer())
                system.drawText('%s to %s' % (inp[:inp.find(' ')], inp[inp.find(' ')+1:]), system.getFontMedium(), system.getBlack(), system.getScreen(), 600, 45)
                if controller.getSpace():
                    system.drawId(controller.getNodes())
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
                        elif event.key == K_SPACE:
                            controller.setSpace(not controller.getSpace())

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
                # Update view
                system.fillWhite()
                system.drawGUI()
                system.drawAIbuttons(controller.getP1AI(), controller.getP2AI())
                system.updateEdges2(controller.getEdges(), controller.getThickness())
                system.updateNeighbours(triLogic.getNeighbours(), 12)
                system.updateNodes(controller.getNodes(), controller.getSize())
                system.displayPlayer(controller.getPlayer())

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
                    elif event.key == K_SPACE:
                        controller.setSpace(not controller.getSpace())
                    elif event.key == K_c:
                        controller.setC(not controller.getC())
                    elif event.key == K_l:
                        controller.setL(not controller.getL())

                # Mouse action -----------------------------
                elif event.type == MOUSEBUTTONDOWN:

                    # Check if the buttons are pressed ------
                    if system.getBackButton().collidepoint(pygame.mouse.get_pos()):
                        return 0
                    elif system.getRestartButton().collidepoint(pygame.mouse.get_pos()):
                        return 1

                    # Enable AI player 1 ----------------------------
                    elif system.getP1AIButton().collidepoint(pygame.mouse.get_pos()):
                        controller.toggleP1ai()

                    # Enable AI player 2 ----------------------------
                    elif system.getP2AIButton().collidepoint(pygame.mouse.get_pos()):
                        controller.toggleP2ai()

                    # No active node ------------------------
                    elif controller.getActivePos() is None:
                        for node in controller.getNodes():
                            if controller.nodeCollision(node, mousePos, "node"):
                                if len(node.getRelations()) < 3:
                                    controller.setActiveNode(node)
                                    controller.setActivePos(controller.getActiveNode().getPos())
                                    node.getRelations().append(-1)
                                    triLogic.setNeighbours(triLogic.dt.exportNeighbours(node.getPos(), "node",
                                                                                        triLogic.getChosenCenter(),
                                                                                        controller.getActiveNode().getPos()))

                    # Active node ---------------------------
                    elif controller.getActivePos() is not None:

                        # Select centroid -------------------
                        for centerNode in triLogic.getCentroids():
                            if centerNode in triLogic.getNeighbours():
                                if controller.nodeCollision(centerNode, mousePos, "centerNode"):
                                    triLogic.getChosenCenter().append(centerNode)

                                    triLogic.getNeighbours().clear()
                                    triLogic.setNeighbours(
                                        triLogic.dt.exportNeighbours(centerNode, "centerNode",
                                                                     triLogic.getChosenCenter(),
                                                                     controller.getActiveNode().getPos()))

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
                                            mid = triLogic.getChosenCenter()[
                                                int(len(triLogic.getChosenCenter()) / 2)]
                                        else:
                                            mid = [(controller.getActivePos()[0] + mousePos[0]) / 2,
                                                   (controller.getActivePos()[1] + mousePos[1]) / 2]
                                        controller.addNode(mid[0], mid[1])

                                        # Remove placeholder relation
                                        controller.getActiveNode().getRelations().remove(-1)

                                        # Add relations between connected nodes
                                        controller.getActiveNode().getRelations().append(
                                            controller.getNodes()[-1].getId())
                                        controller.getNodes().__getitem__(node.getId()).getRelations().append(
                                            controller.getNodes()[-1])
                                        controller.getNodes().__getitem__(-1).getRelations().append(
                                            controller.getActiveNode())
                                        controller.getNodes().__getitem__(-1).getRelations().append(node)

                                        # Add new path and node
                                        triLogic.dt.addPath(controller.getActiveNode().getPos(), node.getPos(),
                                                            triLogic.getChosenCenter(), mid)
                                        triLogic.updateCentroids()

                                        minRadius = triLogic.dt.exportMinRadius()
                                        if minRadius < controller.getSize():
                                            controller.setSize(math.floor(minRadius))
                                            triLogic.setCentersize((math.floor(minRadius * 2 / 3)))

                                        triLogic.clearChosenCenter()
                                        triLogic.clearNeighbours()

                                        controller.getTempEdge().clear()
                                        controller.setActiveNode(None)
                                        controller.setActivePos(None)

                                        controller.setTurn(controller.getTurn() + 1)

                                    # Check if game is over
                                    if controller.getTurn() == 3 * amount - 1:
                                        controller.setDone(True)
                                    elif controller.getTurn() >= 2 * amount:
                                        unlockedNodes = []
                                        Check = True
                                        pygame.time.delay(1000)
                                        controller.setDone(True)
                                        for node in controller.getNodes():
                                            if len(node.getRelations()) < 2:
                                                Check = False
                                                break
                                            elif len(node.getRelations()) < 3:
                                                unlockedNodes.append(node)
                                        if Check:
                                            for i, uNode1 in enumerate(unlockedNodes):
                                                for uNode2 in unlockedNodes[i + 1:]:
                                                    paths = pathfinding(triLogic.dt, uNode1.getPos(),
                                                                        uNode2.getPos()).getPaths()
                                                    if len(paths) > 0:
                                                        controller.setDone(False)
                                                        break
                                                if not controller.getDone():
                                                    break
                                                elif i == len(unlockedNodes) - 1:
                                                    controller.setDone(True)

                                    # Remove placeholder relation
                                    controller.removePlaceholder()

                # -------------------------------------------------------------------
                # ------------------------------- AI --------------------------------
                # -------------------------------------------------------------------
                if (controller.getP1AI() and (controller.getPlayer() == 1)) or \
                        (controller.getP2AI() and (controller.getPlayer() == 2)):

                    # Initialize AI
                    ai = AI()

                    # Find nodes that are eligible
                    legalNodes = ai.getLegalNodes(controller.getNodes())
                    path = None

                    # ALL PATHS APPROACH -----------------------

                    if 0 == 1:
                        allPaths = []
                        path = None

                        for node in legalNodes:
                            s = node

                            for node in legalNodes:
                                e = node

                                paths = pathfinding(triLogic.dt, s.getPos(), e.getPos()).getPaths()

                                for path in paths:
                                    allPaths.append(path)

                        if allPaths != []:
                            if allPaths[0] is not None:
                                path = allPaths[0]

                        # SNIPING PATHS BUT STILL CHECKING ALL IN CASE APPROACH  -----------------------

                        path = None

                        # Find random start and end node
                        r1 = ai.getRandom(len(legalNodes) - 1)
                        for i in range(len(legalNodes), r1):
                            s = legalNodes[i]

                            if len(s.relations) > 1:
                                legalNodes.remove(s)

                            r2 = ai.getRandom(len(legalNodes) - 1)
                            for j in range(len(legalNodes), r2):
                                e = legalNodes[j]
                                paths = pathfinding(triLogic.dt, s.getPos(), e.getPos()).getPaths()
                                if paths is not None:
                                    path = ai.getShortestPath(paths)
                                    break

                            if r2 != 0:
                                for j in range(r2):
                                    e = legalNodes[j]
                                    paths = pathfinding(triLogic.dt, s.getPos(), e.getPos()).getPaths()
                                    if paths is not None:
                                        path = ai.getShortestPath(paths)
                                        break

                        if r1 != 0:
                            for i in range(r1):
                                s = legalNodes[i]

                                if len(s.relations) > 1:
                                    legalNodes.remove(s)

                                r2 = ai.getRandom(len(legalNodes) - 1)
                                for j in range(len(legalNodes), r2):
                                    e = legalNodes[j]
                                    paths = pathfinding(triLogic.dt, s.getPos(), e.getPos()).getPaths()
                                    if paths is not None:
                                        path = ai.getShortestPath(paths)
                                        break

                                if r2 != 0:
                                    for j in range(r2):
                                        e = legalNodes[j]
                                        paths = pathfinding(triLogic.dt, s.getPos(), e.getPos()).getPaths()
                                        if paths is not None:
                                            path = ai.getShortestPath(paths)
                                            break

                    # FIND SHORTEST PATH APPROACH -----------------------
                    # Get random legal start-node

                    if len(legalNodes) - 1 != 0:
                        s = legalNodes[ai.getRandom(len(legalNodes) - 1)]

                    if len(legalNodes) - 1 != 0:
                        e = legalNodes[ai.getRandom(len(legalNodes) - 1)]

                    paths = pathfinding(triLogic.dt, s.getPos(), e.getPos()).getPaths()

                    path = ai.getShortestPath(paths)

                    if path is not None:
                        if len(paths) > 0:
                            for j, point in enumerate(path):
                                if not j == 0:
                                    controller.getEdges().append([path[j - 1], point])

                                    if not point == path[-1]:
                                        triLogic.getChosenCenter().append(point)

                            if len(triLogic.getChosenCenter()) > 0:
                                mid = triLogic.getChosenCenter()[int(len(triLogic.getChosenCenter()) / 2)]
                            else:
                                mid = [(s.getX() + e.getX()) / 2, (s.getY() + e.getY()) / 2]
                            controller.addNode(mid[0], mid[1])

                            # Add relations between connected nodes
                            s.getRelations().append(controller.getNodes()[-1].getId())
                            e.getRelations().append(controller.getNodes()[-1])
                            controller.getNodes().__getitem__(-1).getRelations().append(s)
                            controller.getNodes().__getitem__(-1).getRelations().append(e)

                            # Add new path and node // CRASHER???
                            triLogic.dt.addPath(s.getPos(), e.getPos(), triLogic.getChosenCenter(), mid)

                            minRadius = triLogic.dt.exportMinRadius()
                            if minRadius < controller.getSize():
                                controller.setSize(math.floor(minRadius))
                                triLogic.setCentersize((math.floor(minRadius * 2 / 3)))

                            # Update view
                            triLogic.updateCentroids()
                            triLogic.clearChosenCenter()

                            # Next turn
                            controller.setTurn(controller.getTurn() + 1)

                            # Check if game is over
                            if controller.getTurn() == 3 * amount - 1:
                                controller.setDone(True)
                            elif controller.getTurn() >= 2 * amount:
                                unlockedNodes = []
                                Check = True
                                pygame.time.delay(1000)
                                controller.setDone(True)
                                for node in controller.getNodes():
                                    if len(node.getRelations()) < 2:
                                        Check = False
                                        break
                                    elif len(node.getRelations()) < 3:
                                        unlockedNodes.append(node)
                                if Check:
                                    for i, uNode1 in enumerate(unlockedNodes):
                                        for uNode2 in unlockedNodes[i + 1:]:
                                            paths = pathfinding(triLogic.dt, uNode1.getPos(),
                                                                uNode2.getPos()).getPaths()
                                            if len(paths) > 0:
                                                controller.setDone(False)
                                                break
                                        if not controller.getDone():
                                            break
                                        elif i == len(unlockedNodes) - 1:
                                            controller.setDone(True)

            # Update view
            system.fillWhite()
            system.drawGUI()
            system.drawAIbuttons(controller.getP1AI(), controller.getP2AI())
            if controller.getL():
                system.updateTriLines(triLogic.dt.getAllEdges(), controller.getThickness())
            system.updateEdges2(controller.getEdges(), controller.getThickness())
            if controller.getC():
                system.updateCentroids(triLogic.getCentroids(), triLogic.getCentersize())
            system.updateNeighbours(triLogic.getNeighbours(), 12)
            system.updateNodes(controller.getNodes(), controller.getSize())
            system.displayPlayer(controller.getPlayer())
            if controller.getSpace():
                system.drawId(controller.getNodes())

            pygame.display.update()
