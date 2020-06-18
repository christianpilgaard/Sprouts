import math


class Point:
    def __init__(self, point, nodeType):
        self.x = point[0]
        self.y = point[1]
        self.coordinates = point
        self.type = nodeType
        self.pointInEdges = []
        self.pointInTriangles = []
        self.centerInTriangle = []
        self.connectable = True
        self.relations = 0

    def getCoordinates(self):
        return self.coordinates

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getType(self):
        return self.type

    def getPointInEdges(self):
        return self.pointInEdges

    def getPointInTriangles(self):
        return self.pointInTriangles

    def getCenterInTriangle(self):
        return self.centerInTriangle

    def setCenterInTriangle(self, centerInTriangle):
        self.centerInTriangle = centerInTriangle

    def getConnectable(self):
        return self.connectable

    def setConnectable(self, connectable):
        self.connectable = connectable

    def getRelations(self):
        return self.relations

    def setRelations(self, relations):
        self.relations = relations

    def addRelations(self, extraRelations):
        self.setRelations(self.getRelations() + extraRelations)
        if self.getRelations() == 3:
            self.setConnectable(False)


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.edgeInTriangles = []
        self.drawn = False

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getEdgeInTriangles(self):
        return self.edgeInTriangles

    def getDrawn(self):
        return self.drawn

    def setDrawn(self, drawn):
        self.drawn = drawn


class Triangle:
    def __init__(self, point1, point2, point3, edge1, edge2, edge3):
        self.points = (point1, point2, point3)
        self.edges = (edge1, edge2, edge3)
        self.center = Point(self.calculateCenter([point1, point2, point3]), "centerNode")
        self.center.setCenterInTriangle(self)

    def getPoints(self):
        return self.points

    def getEdges(self):
        return self.edges

    def getCenter(self):
        return self.center

    def calculateCenter(self, tri):
        A = tri[2]
        B = tri[1]
        C = tri[0]
        a = math.sqrt(abs((tri[0].getX()) - (tri[1].getX())) ** 2 + abs((tri[0].getY()) - (tri[1].getY())) ** 2)
        b = math.sqrt(abs((tri[0].getX()) - (tri[2].getX())) ** 2 + abs((tri[0].getY()) - (tri[2].getY())) ** 2)
        c = math.sqrt(abs((tri[1].getX()) - (tri[2].getX())) ** 2 + abs((tri[1].getY()) - (tri[2].getY())) ** 2)

        center = [((a * A.getX()) + (b * B.getX()) + (c * C.getX())) / (a + b + c), ((a * A.getY()) + (b * B.getY()) + (c * C.getY())) / (a + b + c)]
        return center


class Triangulation(Point, Edge, Triangle):
    def __init__(self):
        self.allPoints = []
        self.allEdges = []
        self.allTriangles = []
        self.deadEnds = []

    def getAllPoints(self):
        return self.allPoints

    def setAllPoints(self, allPoints):
        self.allPoints = allPoints

    def getAllEdges(self):
        return self.allEdges

    def setAllEdges(self, allEdges):
        self.allEdges = allEdges

    def getAllTriangles(self):
        return self.allTriangles

    def setAllTriangles(self, allTriangles):
        self.allTriangles = allTriangles

    def getDeadEnds(self):
        return self.deadEnds

    def setDeadEnds(self, deadEnds):
        self.deadEnds = deadEnds

    def resetTriangulation(self):
        self.setAllPoints([])
        self.setAllEdges([])
        self.setAllTriangles([])
        self.setDeadEnds([])

    def addCornerNodes(self):
        self.addPoint([800, 800])
        self.addPoint([1, 100])
        self.addPoint([800, 100])
        self.addPoint([1, 800])

        co1 = self.getPoint([800, 800])
        co1.setConnectable(False)

        co2 = self.getPoint([1, 100])
        co2.setConnectable(False)

        co3 = self.getPoint([800, 100])
        co3.setConnectable(False)

        co4 = self.getPoint([1, 800])
        co4.setConnectable(False)

    def exportInCenters(self):
        centers = []
        for tri in self.getAllTriangles():
            c = tri.getCenter()
            centers.append([c.getX(), c.getY()])

        return centers

    def orientation(self, p, q, r):
        # to find the orientation of an ordered triplet (p,q,r)
        # function returns the following values:
        # 0 : Colinear points
        # 1 : Clockwise points
        # 2 : Counterclockwise

        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if (val > 0):

            # Clockwise orientation
            return 1
        elif (val < 0):

            # Counterclockwise orientation
            return 2
        else:

            # Colinear orientation
            return 0

    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    def doIntersect(self, p1, q1, p2, q2):

        # Find the 4 orientations
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        # intersect is true
        if ((o1 != o2) and (o3 != o4)):
            return True

        # else not intersect
        return False

    def addPoint(self, currentPoint):
        pointAsPoint = Point(currentPoint, "node")
        connections = []
        for point in self.getAllPoints():
            intersect = False

            # Check if an edge between currentPoint and another point intersect with an existed edge
            for edge in self.getAllEdges():
                if self.doIntersect(currentPoint, point.getCoordinates(), edge.getStart().getCoordinates(), edge.getEnd().getCoordinates()):
                    # Intersect in the starting or ending points is allowed
                    if ((point.getCoordinates() == edge.getStart().getCoordinates()) or (point.getCoordinates() == edge.getEnd().getCoordinates())
                            or (currentPoint == edge.getStart().getCoordinates()) or (currentPoint == edge.getEnd().getCoordinates())):
                        continue
                    else:
                        intersect = True
                        break
            # Add new edge, if it not collide in the existed edges
            if not intersect:
                newEdge = Edge(pointAsPoint, point)
                self.getAllEdges().append(newEdge)
                pointAsPoint.getPointInEdges().append(newEdge)
                point.getPointInEdges().append(newEdge)
                connections.append(point)

        # if there are more than 1 connection will there be minimum 1 new triangle
        if len(connections) > 1:
            for i, point in enumerate(connections):
                for point2 in connections[(i + 1):]:
                    for edgeConnect in point.getPointInEdges():
                        if edgeConnect in point2.getPointInEdges():
                            # Check if there are a point inside
                            pInside = False
                            for tri in edgeConnect.getEdgeInTriangles():
                                for p in tri.getPoints():
                                    if p == point or p == point2:
                                        continue
                                    if p in connections:
                                        pInside = self.pointInsideTriangle(point, point2, pointAsPoint, p)
                            if not pInside:
                                self.addTriangle(pointAsPoint, point, point2)

        self.getAllPoints().append(pointAsPoint)

    def addPath(self, start, end, inCenters, midPoint):
        if len(inCenters) < 2:
            p1 = self.getPoint(start)
            p2 = self.getPoint(end)

            if len(inCenters) == 0:
                oldEdge = self.getEdge(p1, p2)

                # Delete triangles with this edge
                for tri in oldEdge.getEdgeInTriangles():
                    self.deleteTriangle(tri, [oldEdge])
                self.deleteEdge(oldEdge)
            else:
                center = self.getCenter(inCenters[0])
                self.deleteTriangle(center.getCenterInTriangle(), [])

            # Add midpoint, new edges and triangles
            self.addPoint(midPoint)

            # mark the the drawn edges
            mid = self.getPoint(midPoint)
            newEdge1 = self.getEdge(p1, mid)
            newEdge2 = self.getEdge(mid, p2)

            newEdge1.setDrawn(True)
            newEdge2.setDrawn(True)

            p1.addRelations(1)
            p2.addRelations(1)
            mid.addRelations(2)

        if len(inCenters) > 1:
            # Add first centroid
            center = self.getCenter(inCenters[0])
            self.deleteTriangle(center.getCenterInTriangle(), [])

            self.addPoint(inCenters[0])

            p1 = self.getPoint(start)
            p2 = self.getPoint(inCenters[0])
            p2.setConnectable(False)
            newEdge = self.getEdge(p1, p2)

            # mark the the first drawn edge
            newEdge.setDrawn(True)
            p1.addRelations(1)
            p2.addRelations(1)

            # update triangulation with one more centroid one at a time
            for i, c in enumerate(inCenters):
                if (i > 0):
                    c2 = c
                    c1 = inCenters[i - 1]
                    # Find the edge that colide with the connection of the two centroids
                    for oldEdge in self.getAllEdges():
                        if self.doIntersect(c1, c2, oldEdge.getStart().getCoordinates(), oldEdge.getEnd().getCoordinates()):

                            # Delete triangles with this edge
                            for tri in oldEdge.getEdgeInTriangles():
                                self.deleteTriangle(tri, [oldEdge])
                            self.deleteEdge(oldEdge)
                            break

                    self.addPoint(c2)

                    po1 = self.getPoint(c1)
                    po2 = self.getPoint(c2)
                    if c2 != midPoint:
                        po2.setConnectable(False)
                    newEdge = self.getEdge(po1, po2)

                    # mark the the drawn edge
                    newEdge.setDrawn(True)
                    po1.addRelations(1)
                    po2.addRelations(1)

            # Mark the last drawn edge
            pt1 = self.getPoint(inCenters[-1])
            pt2 = self.getPoint(end)
            newEdge = self.getEdge(pt1, pt2)

            newEdge.setDrawn(True)
            pt1.addRelations(1)
            pt2.addRelations(1)

    def getTriangle(self, points):
        point1 = points[0]
        point2 = points[1]
        point3 = points[2]
        for tri in self.getAllTriangles():
            if (tri.getPoints() == (point1, point2, point3) or tri.getPoints() == (point1, point3, point2) or
                    tri.getPoints() == (point2, point1, point3) or tri.getPoints() == (point2, point3, point1) or
                    tri.getPoints() == (point3, point1, point2) or tri.getPoints() == (point3, point2, point1)):
                return tri

    def deleteTriangle(self, tri, saveEdge):
        (e1, e2, e3) = tri.getEdges()
        (p1, p2, p3) = tri.getPoints()

        if len(saveEdge) > 0:
            for e in [e1, e2, e3]:
                if (e != saveEdge[0]):
                    e.getEdgeInTriangles().remove(tri)
        else:
            e1.getEdgeInTriangles().remove(tri)
            e2.getEdgeInTriangles().remove(tri)
            e3.getEdgeInTriangles().remove(tri)

        p1.getPointInTriangles().remove(tri)
        p2.getPointInTriangles().remove(tri)
        p3.getPointInTriangles().remove(tri)

        self.getAllTriangles().remove(tri)

    def addTriangle(self, p1, p2, p3):
        edge1, edge2, edge3 = self.getEdges(p1, p2, p3)

        # Make new triangle
        newTriangle = Triangle(p1, p2, p3, edge1, edge2, edge3)
        # Add triangle to Triangulation memory
        self.getAllTriangles().append(newTriangle)

        # Add triangle to points and edges
        p1.getPointInTriangles().append(newTriangle)
        p2.getPointInTriangles().append(newTriangle)
        p3.getPointInTriangles().append(newTriangle)
        edge1.getEdgeInTriangles().append(newTriangle)
        edge2.getEdgeInTriangles().append(newTriangle)
        edge3.getEdgeInTriangles().append(newTriangle)

    def pointInsideTriangle(self, p1, p2, p3, mid):
        if (((p1.getX() > mid.getX()) and (p2.getX() > mid.getX()) and (p3.getX() > mid.getX())) or
                ((p1.getX() < mid.getX()) and (p2.getX() < mid.getX()) and (p3.getX() < mid.getX())) or
                ((p1.getY() > mid.getY()) and (p2.getY() > mid.getY()) and (p3.getY() > mid.getY())) or
                ((p1.getY() < mid.getY()) and (p2.getY() < mid.getY()) and (p3.getY() < mid.getY()))):
            return False
        else:
            return True

    def getEdges(self, point1, point2, point3):
        edges = []
        for edge in self.getAllEdges():
            if (edge.getStart().getCoordinates() == point1.getCoordinates() and edge.getEnd().getCoordinates() == point2.getCoordinates()) or (
                    edge.getStart().getCoordinates() == point2.getCoordinates() and edge.getEnd().getCoordinates() == point1.getCoordinates()):
                edges.append(edge)
            elif (edge.getStart().getCoordinates() == point1.getCoordinates() and edge.getEnd().getCoordinates() == point3.getCoordinates()) or (
                    edge.getStart().getCoordinates() == point3.getCoordinates() and edge.getEnd().getCoordinates() == point1.getCoordinates()):
                edges.append(edge)
            elif (edge.getStart().getCoordinates() == point3.getCoordinates() and edge.getEnd().getCoordinates() == point2.getCoordinates()) or (
                    edge.getStart().getCoordinates() == point2.getCoordinates() and edge.getEnd().getCoordinates() == point3.getCoordinates()):
                edges.append(edge)
            # Stop search if all edges are found
            if len(edges) == 3:
                break
        return edges

    def getEdge(self, point1, point2):
        for edge in self.getAllEdges():
            if (edge.getStart().getCoordinates() == point1.getCoordinates() and edge.getEnd().getCoordinates() == point2.getCoordinates()) or (
                    edge.getStart().getCoordinates() == point2.getCoordinates() and edge.getEnd().getCoordinates() == point1.getCoordinates()):
                return edge

    def deleteEdge(self, edge):
        (p1, p2) = edge.getStart(), edge.getEnd()

        p1.getPointInEdges().remove(edge)
        p2.getPointInEdges().remove(edge)

        self.getAllEdges().remove(edge)

    def getPoint(self, point):
        for p in self.getAllPoints():
            if (int(p.getX()) == int(point[0])) and (int(p.getY()) == int(point[1])):
                return p

    def getCenter(self, point):
        for tri in self.getAllTriangles():
            c = tri.getCenter()
            if (c.getX() == point[0]) and (c.getY() == point[1]):
                return c

    def exportNeighbours(self, coords, typeOfNode, alreadyChosen, startNode):
        Neighbours = []
        if typeOfNode == "node":
            chosenPoint = self.getPoint(coords)
            # Add all points where there are an edge between and the centroid for the triangles the point is a part of
            for edge in self.getAllEdges():
                if not edge.getDrawn():
                    if edge.getStart() == chosenPoint and edge.getEnd().getConnectable():
                        Neighbours.append(edge.getEnd().getCoordinates())
                    elif edge.getEnd() == chosenPoint and edge.getStart().getConnectable():
                        Neighbours.append(edge.getStart().getCoordinates())
            for tri in chosenPoint.getPointInTriangles():
                Neighbours.append([tri.getCenter().getX(), tri.getCenter().getY()])
        elif typeOfNode == "centerNode":
            # Add all points of the triangle the centroid is in and the centroids in the neighbouring triangles
            center = self.getCenter(coords)
            tri = center.getCenterInTriangle()
            for point in tri.getPoints():
                if point.getConnectable():
                    Neighbours.append(point.getCoordinates())
            for edge in tri.getEdges():
                if not edge.getDrawn():
                    for triangle in edge.getEdgeInTriangles():
                        if triangle != tri:
                            if [triangle.getCenter().getX(), triangle.getCenter().getY()] not in alreadyChosen:
                                Neighbours.append([triangle.getCenter().getX(), triangle.getCenter().getY()])
        if startNode:
            if startNode in Neighbours:
                # remove startnode, if there are only chosen 1 centroid = no loop
                # or if the startnode had 2 relations before pressed on it
                if len(alreadyChosen) < 2:
                    Neighbours.remove(startNode)
                else:
                    p = self.getPoint(startNode)
                    if p.getRelations() + 1 == 3:
                        Neighbours.remove(startNode)
        return Neighbours

    """
    def findDeadEnds(self, centers):
        acceptedCenters = []
        for center in centers:
            neighbours = self.exportNeighbours(center, "centerNode", [], [])
            if len(neighbours) < 2:
                self.deadEnds.append(center)
            else:
                count = len(neighbours)
                for n in neighbours:
                    if (n in self.deadEnds):
                        if(count - 1) < 2:
                            self.deadEnds.append(center)
                            if n in acceptedCenters:
                                acceptedCenters.remove(n)
                                self.deadEnds.append(n)
                        else:
                            count -= 1
                if count > 1:
                    acceptedCenters.append(center)
        return acceptedCenters
    """
