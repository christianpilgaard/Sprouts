class pathfinding:
    def __init__(self, triangulation, start, goal):

        self.tri = triangulation
        self.start = start
        self.goal = goal

        # Create list of paths
        self.paths = self.BFS()

    def getTri(self):
        return self.tri

    def getStart(self):
        return self.start

    def getGoal(self):
        return self.goal

    def getPaths(self):
        return self.paths

    def BFS(self):
        # Mark all the vertices as not visited
        visited = {}
        for i in self.getTri().getAllPoints():
            visited[str([i.getX(), i.getY()])] = False
        for j in self.getTri().exportInCenters():
            visited[str(j)] = False


        # Create a queue for BFS
        queue = []
        paths = []

        # Mark the source node as
        # visited and enqueue it
        if not self.getStart() == self.getGoal():
            visited[str(self.getStart())] = True

        for i in self.getTri().exportNeighbours(self.getStart(), self.getType(self.getStart()), [self.getStart()], self.getStart()):
            if i == self.getGoal():
                path = [self.getStart()]
                path.append(i)
                paths.append(path)
            elif self.getType(i) == "centerNode":
                path = [self.getStart()]
                path.append(i)
                v = visited.copy()
                v[str(i)] = True
                queue.append([path, v])


        while queue:

            # Dequeue a vertex from
            # queue and print it
            p, visited = queue.pop(0)
            n = p[-1]


            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it

            for i in self.getTri().exportNeighbours(n, self.getType(n), p, self.getStart()):
                if not visited[str(i)]:
                    if i == self.getGoal():
                        path = p.copy()
                        path.append(i)
                        paths.append(path)
                    elif self.getType(i) == "centerNode":
                        path = p.copy()
                        path.append(i)
                        #v = visited.copy()
                        visited[str(i)] = True
                        queue.append([path, visited])


        return paths

    def getType(self, point):
        if not self.getTri().getPoint(point) is None:
            type = "node"
        else:
            type = "centerNode"
        return type
