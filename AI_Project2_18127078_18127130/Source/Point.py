import math
import copy as cp
from random import randint


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y

    def __str__(self):
        return str((self.x, self.y))

    def rand(self, sos):
        self.x = randint(0, sos)
        self.y = randint(0, sos)

    def manhattan_distance(self, another):
        return abs(self.x - another.x) + abs(self.y - another.y)

    def euclid_distance(self, another):
        return math.sqrt((self.x - another.x) ** 2 + (self.y - another.y) ** 2)

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

    def adj(self):
        return self.up(), self.down(), self.left(), self.right()

    def top_left(self):
        return self.up().left()

    def top_right(self):
        return self.up().right()

    def bot_left(self):
        return self.down().left()

    def bot_right(self):
        return self.down().right()

    def diag(self):
        return self.top_left(), self.top_right(), self.bot_left(), self.bot_right()

    def clone(self):
        return cp.deepcopy(self)