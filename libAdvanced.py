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
def playGame(amount, txt, txt_input):
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

            if len(s.relations) < 3 and len(e.relations) < 3:
                paths = pathfinding(TriangulationLogic.dt, [s.x, s.y], [e.x, e.y]).paths

                if len(paths) > 0:
                    print("more moves")
                    i = random.randint(0, len(paths) - 1)

                    for j, point in enumerate(paths[i]):
                        if not j == 0:
                            controller.edges.append([paths[i][j - 1], point])
                            if not point == paths[i][-1]:
                                triLogic.chosenCenter.append(point)

                    if len(triLogic.chosenCenter) > 0:
                        mid = triLogic.chosenCenter[int(len(triLogic.chosenCenter) / 2)]
                    else:
                        mid = [(s.x + e.x) / 2,
                               (s.y + e.y) / 2]
                    controller.addNode(mid[0], mid[1])

                    # Add relations between connected nodes
                    s.relations.append(e.id)
                    e.relations.append(s.id)

                    # Add new path and node
                    triLogic.dt.addPath([s.x, s.y], [e.x, e.y], triLogic.chosenCenter, mid)
                    triLogic.updateCentroids(triLogic.getCentroids(), triLogic.getCentersize())
                    triLogic.clearChosenCenter()

                    controller.setTurn(controller.getTurn() + 1)

                    system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.centroids,
                                         triLogic.dt.allEdges,
                                         triLogic.neighbours, controller.size, triLogic.getCentersize(), 5,
                                         controller.getPlayer())
                    pygame.display.update()

                else:
                    controller.error = True
                    break

            time.sleep(2.0)

        while controller.error:
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
        if controller.done:
            system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.centroids, triLogic.dt.allEdges,
                                 triLogic.neighbours, controller.size, triLogic.getCentersize(), 5,
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
                    return 1

            # Mouse action -----------------------------
            elif event.type == MOUSEBUTTONDOWN:

                # Check if the buttons are pressed ------
                if system.back_button.collidepoint(pygame.mouse.get_pos()):
                    return 0
                elif system.restart_button.collidepoint(pygame.mouse.get_pos()):
                    return 1

                # No active node ------------------------
                if controller.getActivePos() is None:
                    for node in controller.getNodes():
                        if controller.nodeCollision(node, mousePos, "node"):
                            if len(node.relations) < 3:
                                controller.setActiveNode(node)
                                controller.setActiveItem(node.id)
                                controller.setActivePos([controller.getActiveNode().x, controller.getActiveNode().y])
                                node.relations.append(-1)
                                triLogic.neighbours = triLogic.dt.exportNeighbours([node.x, node.y], "node", triLogic.chosenCenter, [controller.getActiveNode().x, controller.getActiveNode().y])

                # Active node ---------------------------
                if controller.getActivePos() is not None:

                    # Select centroid -------------------
                    for centerNode in triLogic.centroids:
                        if centerNode in triLogic.neighbours:
                            if controller.nodeCollision(centerNode, mousePos, "centerNode"):
                                controller.edges.append([controller.getActivePos(), centerNode])
                                controller.setActivePos(centerNode)
                                triLogic.chosenCenter.append(centerNode)

                                triLogic.neighbours.clear()
                                triLogic.neighbours = triLogic.dt.exportNeighbours(centerNode,
                                        "centerNode", triLogic.chosenCenter, [controller.getActiveNode().x, controller.getActiveNode().y])

                    # Select end node ------------------
                    for node in controller.getNodes():
                        if controller.nodeCollision(node, mousePos, "node"):
                            if [node.x, node.y] in triLogic.neighbours:
                                if len(node.relations) < 3:
                                    controller.edges.append([controller.getActivePos(), [node.x, node.y]])

                                    if len(triLogic.chosenCenter) > 0:
                                        mid = triLogic.chosenCenter[int(len(triLogic.chosenCenter) / 2)]
                                    else:
                                        mid = [(controller.getActivePos()[0] + mousePos[0]) / 2, (controller.getActivePos()[1] + mousePos[1]) / 2]
                                    controller.addNode(mid[0], mid[1])

                                    # Remove placeholder relation
                                    controller.nodes.__getitem__(controller.getActiveItem()).relations.remove(-1)

                                    # Add relations between connected nodes
                                    controller.nodes.__getitem__(controller.getActiveItem()).relations.append(controller.nodes[-1].id)
                                    controller.nodes.__getitem__(node.id).relations.append(controller.nodes[-1].id)
                                    controller.nodes.__getitem__(-1).relations.append(controller.getActiveItem())
                                    controller.nodes.__getitem__(-1).relations.append(node.id)

                                    # Add new path and node
                                    triLogic.dt.addPath([controller.getActiveNode().x, controller.getActiveNode().y], [node.x, node.y], triLogic.chosenCenter, mid)
                                    triLogic.updateCentroids()
                                    triLogic.clearChosenCenter()
                                    triLogic.clearNeighbours()

                                    controller.setActiveNode(None)
                                    controller.setActivePos(None)
                                    controller.setActiveItem(None)

                                # Remove placeholder relation
                                controller.removePlaceholder()

                                # win detection
                                if controller.getTurn() == 3 * amount - 1:
                                    print("True")
                                    controller.done = True
                                elif controller.getTurn() >= 2 * amount:
                                    unlockedNodes = []
                                    Check = True
                                    controller.done = False
                                    for node in controller.getNodes():
                                        if len(node.relations) < 2:
                                            Check = False
                                            break
                                        elif len(node.relations) < 3:
                                            unlockedNodes.append(node)
                                    if Check:
                                        for i, uNode in enumerate(unlockedNodes):
                                            if not i == 0:
                                                paths = pathfinding(TriangulationLogic.dt,
                                                                    [unlockedNodes[i - 1].x, unlockedNodes[i - 1].y],
                                                                    [uNode.x, uNode.y]).paths
                                                if len(paths) > 0:
                                                    controller.done = False
                                                    break
                                                elif i == len(unlockedNodes) - 1:
                                                    controller.done = True

        system.updateScreen2(controller.getNodes(), controller.getEdges(), triLogic.centroids, triLogic.dt.allEdges,
                             triLogic.neighbours, controller.size, triLogic.getCentersize(), 5, controller.getPlayer())
        pygame.display.update()


# ------------------------------------------------
# Initialize classes
system = System()
controller = GameController()
triLogic = TriangulationLogic()