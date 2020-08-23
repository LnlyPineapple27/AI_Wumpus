import math
import copy as cp


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y

    def manhattan_distance(self, another):
        return abs(self.x - another.x) + abs(self.y - another.y)

    def euclid_distance(self, another):
        return math.sqrt((self.x - another.x)**2 + (self.y - another.y)**2)

    def coordinate(self):
        return cp.copy(self.x), cp.copy(self.y)

    def up(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.x -= 1
        return cp_pnt
    
    def down(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.x += 1
        return cp_pnt

    def left(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.y -= 1
        return cp_pnt

    def right(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.y += 1
        return cp_pnt
