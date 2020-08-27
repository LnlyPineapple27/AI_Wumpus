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

    def to_string(self):
        return "R{}{}".format(self.x, self.y)

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
    # ADJ kề
    sen = ["(ADJ(x, y) & ADJ(x, z) & B(y) & B(z)) ==> PIT(x)",
           "(ADJ(x, y) & ADJ(x, z) & S(y) & S(z)) ==> WUM(x)",
           "(ADJ(x, y) & NULL(x)) ==> SAFE(y)",
           "B(y) ==> SAFE(y)",
           "S(y) ==> SAFE(y)"]
    # Create an array to hold clauses
    clauses = [utils.expr(s) for s in sen]
    # Create a first-order logic knowledge base (KB) with clauses
    return logic.FolKB(clauses)


def in_map(size, pos):
    return 0 <= pos.x < size and 0 <= pos.y < size


def think(world, KB, cur:Point):
    up = point_to_room(cur.up(), world.map_size).to_string() if in_map(world.map_size, cur.up()) else None
    down = point_to_room(cur.down(), world.map_size).to_string() if in_map(world.map_size, cur.down()) else None
    left = point_to_room(cur.left(), world.map_size).to_string() if in_map(world.map_size, cur.left()) else None
    right = point_to_room(cur.right(), world.map_size).to_string() if in_map(world.map_size, cur.right()) else None
    dir = []
    if up:
        cl = utils.expr("ADJ({}, {})".format(point_to_room(cur, world.map_size).to_string(), up))
        if cl not in KB.clauses:
            KB.tell(cl)
        safe = KB.ask(utils.expr("SAFE({})".format(up)))
        expanded = KB.ask(utils.expr("EXP({})".format(up)))
        print("up, safe:", not not safe)
        print("up, expanded:", not not expanded)
        if safe and not expanded:
            dir.append("Up")
    if down:
        cl = utils.expr("ADJ({}, {})".format(point_to_room(cur, world.map_size).to_string(), down))
        if cl not in KB.clauses:
            KB.tell(cl)
        safe = KB.ask(utils.expr("SAFE({})".format(down)))
        expanded = KB.ask(utils.expr("EXP({})".format(down)))
        print("down, safe:", not not safe)
        print("down, expanded:", not not expanded)
        if safe and not expanded:
            dir.append("Down")
    if left:
        cl = utils.expr("ADJ({}, {})".format(point_to_room(cur, world.map_size).to_string(), left))
        if cl not in KB.clauses:
            KB.tell(cl)
        safe = KB.ask(utils.expr("SAFE({})".format(left)))
        expanded = KB.ask(utils.expr("EXP({})".format(left)))
        print("left, safe:", not not safe)
        print("left, expanded:", not not expanded)
        if safe and not expanded:
            dir.append("Left")
    if right:
        cl = utils.expr("ADJ({}, {})".format(point_to_room(cur, world.map_size).to_string(), right))
        if cl not in KB.clauses:
            KB.tell(cl)
        safe = KB.ask(utils.expr("SAFE({})".format(right)))
        expanded = KB.ask(utils.expr("EXP({})".format(right)))
        print("right, safe:", not not safe)
        print("right, expanded:", not not expanded)
        if safe and not expanded:
            dir.append("Right")
    print("dir",dir)
    return dir