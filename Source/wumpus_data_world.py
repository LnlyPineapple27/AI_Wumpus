from aima import logic
from aima import utils
import copy as cp
from Point import Point

FUNCTION = ["WUM({})", "PIT({})", "EXP({})"]


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
    def __init__(self, pos: RoomCoordinate, sym: str):
        self.position = pos
        self.sym = sym
        self.name = "R{}{}".format(self.position.x, self.position.y)


def init_KB():
    # Init
    # ADJ kề
    sen = ["(ADJ(x, y) & ADJ(x, z) & B(y) & B(z)) ==> PIT(x)",
           "(ADJ(x, y) & ADJ(x, z) & S(y) & S(z)) ==> WUM(x)",
           "(ADJ(x, y) & NULL(x)) ==> SAFE(y)",
           "B(x) ==> SAFE(x)",
           "S(x) ==> SAFE(x)",
           "NULL(x) ==> SAFE(x)"]
    # Create an array to hold clauses
    clauses = [utils.expr(s) for s in sen]
    # Create a first-order logic knowledge base (KB) with clauses
    return logic.FolKB(clauses)


def in_map(size, pos):
    return 0 <= pos.x < size and 0 <= pos.y < size


def KB_asking(KB, room):
    wum = KB.ask(utils.expr("WUM{}".format(room)))
    pit = KB.ask(utils.expr("PIT{}".format(room)))
    safe = KB.ask(utils.expr("SAFE({})".format(room)))
    expanded = KB.ask(utils.expr("EXP({})".format(room)))

    return wum, pit, safe, expanded


def think(world, KB, cur: Point):
    up = point_to_room(cur.up(), world.map_size).to_string() if in_map(world.map_size, cur.up()) else None
    down = point_to_room(cur.down(), world.map_size).to_string() if in_map(world.map_size, cur.down()) else None
    left = point_to_room(cur.left(), world.map_size).to_string() if in_map(world.map_size, cur.left()) else None
    right = point_to_room(cur.right(), world.map_size).to_string() if in_map(world.map_size, cur.right()) else None
    cur_room = point_to_room(cur, world.map_size).to_string()
    act = []
    safe_dict = {"Up": "NO", "Down": "NO", "Left": "NO", "Right": "NO"}
    if up:
        adj = utils.expr("ADJ({}, {})".format(cur_room, up))
        if adj not in KB.clauses:
            KB.tell(adj)

        wum, pit, safe, expanded = KB_asking(KB, up)
        if wum:
            safe_dict["Up"] = "WUM"
            KB.tell(utils.expr("WUM({})".format(up)))
        elif pit:
            safe_dict["Up"] = "PIT"
            KB.tell(utils.expr("PIT({})".format(up)))
        elif safe:
            safe_dict["Up"] = "SAFE"
            if not expanded:
                act.append("Up")
        print("up, expanded:", not not expanded)

    if down:
        adj = utils.expr("ADJ({}, {})".format(cur_room, down))
        if adj not in KB.clauses:
            KB.tell(adj)
        wum, pit, safe, expanded = KB_asking(KB, down)
        if wum:
            safe_dict["Down"] = "WUM"
            KB.tell(utils.expr("WUM({})".format(down)))
        elif pit:
            safe_dict["Down"] = "PIT"
            KB.tell(utils.expr("PIT({})".format(down)))
        elif safe:
            safe_dict["Down"] = "SAFE"
            if not expanded:
                act.append("Down")
        print("down, safe:", not not safe)
        print("down, expanded:", not not expanded)

    if left:
        adj = utils.expr("ADJ({}, {})".format(cur_room, left))
        if adj not in KB.clauses:
            KB.tell(adj)

        wum, pit, safe, expanded = KB_asking(KB, left)
        if wum:
            safe_dict["Left"] = "WUM"
            KB.tell(utils.expr("WUM({})".format(left)))
        elif pit:
            safe_dict["Left"] = "PIT"
            KB.tell(utils.expr("PIT({})".format(left)))
        elif safe:
            safe_dict["Left"] = "SAFE"
            if not expanded:
                act.append("Left")
        print("left, expanded:", not not expanded)

    if right:
        adj = utils.expr("ADJ({}, {})".format(cur_room, right))
        if adj not in KB.clauses:
            KB.tell(adj)
        wum, pit, safe, expanded = KB_asking(KB, right)
        if wum:
            safe_dict["Right"] = "WUM"
            KB.tell(utils.expr("WUM({})".format(right)))
        elif pit:
            safe_dict["Right"] = "PIT"
            KB.tell(utils.expr("PIT({})".format(right)))
        elif safe:
            safe_dict["Right"] = "SAFE"
            if not expanded:
                act.append("Right")
        print("right, expanded:", not not expanded)

    print("dir1", act)
    print(safe_dict)
    if not act:
        print("dir2", act)
        act = [item[0] for item in safe_dict.items() if item[1] == "SAFE"]
    if not act:
        if "B" in world.map_data[cur.x][cur.y]:
            act = ["Go Home"]
        else:
            act = ["Shoot_arrow"]
            dir = [item[0] for item in safe_dict.items() if item[1] == "WUM"]
            act += dir
            return act

    return act
