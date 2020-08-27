from aima import logic
from aima import utils
import copy as cp
from Point import Point


class RoomCoordinate:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y

    def to_point(self, size):
        return Point(size - self.y, self.x - 1)

    def coordinate(self):
        return cp.copy(self.x), cp.copy(self.y)

    def up(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.y += 1
        return cp_pnt

    def down(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.y -= 1
        return cp_pnt

    def left(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.x += 1
        return cp_pnt

    def right(self):
        cp_pnt = cp.deepcopy(self)
        cp_pnt.x -= 1
        return cp_pnt


def point_to_room(pnt: Point, size):
    return RoomCoordinate(pnt.y + 1, size - pnt.x)


class Room:
    def __init__(self, pos:RoomCoordinate, sym:str):
        self.position = pos
        self.sym = sym
        self.name = "R{}{}".format(self.position.x, self.position.y)


def init_KB():
    # Init
    sen = ["(ADJ(x, y) & ADJ(x, z) & B(y) & B(z)) ==> PIT(x)",
           "(ADJ(x, y) & ADJ(x, z) & S(y) & S(z)) ==> WUM(x)"]
    # Create an array to hold clauses
    clauses = [utils.expr(s) for s in sen]
    # Create a first-order logic knowledge base (KB) with clauses
    return logic.FolKB(clauses)