class pathfinding:
    def __init__(self, triangulation, start, goal):

        self.tri = triangulation
        self.start = start
        self.goal = goal

        # Create list of paths
        self.paths = self.BFS()

    def BFS(self):
        # Mark all the vertices as not visited
        visited = {}
        for i in self.tri.allPoints:
            visited[str([i.x, i.y])] = False
        for j in self.tri.exportInCenters():
            visited[str(j)] = False


        # Create a queue for BFS
        queue = []
        paths = []

        # Mark the source node as
        # visited and enqueue it
        if not self.start == self.goal:
            visited[str(self.start)] = True
        queue.append([[self.start], visited])

        while queue:

            # Dequeue a vertex from
            # queue and print it
            p, visited = queue.pop(0)
            n = p[-1]


            # Get all adjacent vertices of the
            # dequeued vertex s. If a adjacent
            # has not been visited, then mark it
            # visited and enqueue it

            for i in self.tri.exportNeighbours(n, self.getType(n), p, self.start):
                if not visited[str(i)]:
                    if i == self.goal:
                        path = p.copy()
                        path.append(i)
                        paths.append(path)
                    elif self.getType(i) == "centerNode":
                        path = p.copy()
                        path.append(i)
                        v = visited.copy()
                        v[str(i)] = True
                        queue.append([path, v])


        return paths

    def getType(self, point):
        if not self.tri.getPoint(point) is None:
            type = "node"
        else:
            type = "centerNode"
        return type
