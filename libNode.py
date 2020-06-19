# ------------------------------------------------
# Node class for initializing and operating on vertices
class Node:
    def __init__(self, id, x, y, relations, locked, selected):
        print("Node ", id, " added.")
        self.id = id
        self.x = x
        self.y = y
        self.relations = relations
        self.locked = locked
        self.selected = selected
        self.pos = [self.x, self.y]

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getRelations(self):
        return self.relations

    def getLocked(self):
        return self.locked

    def getSelected(self):
        return self.selected

    def getPos(self):
        return self.pos
