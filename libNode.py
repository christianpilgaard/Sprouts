

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
