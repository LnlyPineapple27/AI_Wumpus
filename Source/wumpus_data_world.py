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
    sen = ["(ADJ(x, y) & ADJ(x, z) & ADJ(x, t) & ADJ(x, v) & B(y) & B(z) & B(t) & B(v)) ==> PIT(x)",
           "(ADJ(x, y) & ADJ(x, z) & ADJ(x, t) & ADJ(x, t) & S(y) & S(z) & S(t) & S(v)) ==> WUM(x)",
           "(EDGE(x) & ADJ(x, y) & ADJ(x, z) & ADJ(x, t) & S(y) & S(z) & S(t)) ==> WUM(x)",
           "(EDGE(x) & ADJ(x, y) & ADJ(x, z) & ADJ(x, t) & B(y) & B(z) & B(t)) ==> PIT(x)",
           "(CORNER(x) & ADJ(x, y) & ADJ(x, z) & S(y) & S(z)) ==> WUM(x)",
           "(CORNER(x) & ADJ(x, y) & ADJ(x, z) & B(y) & B(z)) ==> PIT(x)",
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
    expanded = utils.expr("EXP({})".format(room)) in KB.clauses

    return wum, pit, safe, expanded


def KB_tell_corner_edge(KB, size, pnt):
    adj = pnt.adj()
    pnt = point_to_room(pnt, size).to_string()
    count_in = sum([1 if in_map(size, d) else 0 for d in adj])
    if count_in == 2:
        fact = utils.expr("CORNER({})".format(pnt))
        if fact not in KB.clauses:
            KB.tell(fact)
    elif count_in == 3:
        fact = utils.expr("EDGE({})".format(pnt))
        if fact not in KB.clauses:
            KB.tell(fact)


def think(world, KB, cur: Point):
    up, down, left, right = cur.adj()
    cur_room = point_to_room(cur, world.map_size).to_string()
    act = []
    safe_dict = {"Up": "NO", "Down": "NO", "Left": "NO", "Right": "NO"}
    if in_map(world.map_size, up):
        # Check corner or edge
        KB_tell_corner_edge(KB, world.map_size, up)
        # Add Adjacent fact
        up = point_to_room(up, world.map_size).to_string()
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

    if in_map(world.map_size, down):

        KB_tell_corner_edge(KB, world.map_size, down)

        down = point_to_room(down, world.map_size).to_string()
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

    if in_map(world.map_size, left):
        KB_tell_corner_edge(KB, world.map_size, left)

        left = point_to_room(left, world.map_size).to_string()
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

    if in_map(world.map_size, right):
        KB_tell_corner_edge(KB, world.map_size, right)

        right = point_to_room(right, world.map_size).to_string()
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
    if act:
        act.append("Move")
    if not act:
        print("dir2", act)
        act = [item[0] for item in safe_dict.items() if item[1] == "SAFE"]
        if act:
            act.append("Move")
    if not act:
        if "B" in world.map_data[cur.x][cur.y]:
            act = ["Go_Home"]
        else:
            act = ["Shoot_arrow"]
            dir = [item[0] for item in safe_dict.items() if item[1] == "WUM"]
            if not dir:
                dir = ["Up", "Down", "Left", "Right"]
            act += dir

    print(act)
    return act

