from aima import logic
from aima import utils
import copy as cp
from path_search import *
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

    return wum, pit, safe


def find_safe(world, KB):
    safe_list = []
    s_list = []
    for i in range(world.map_size):
        for j in range(world.map_size):
            p = Point(i, j)
            room = point_to_room(size=world.map_size, pnt=p).to_string()
            cl1 = utils.expr("SAFE({})".format(room))
            cl2 = utils.expr("EXP({})".format(room))
            safe = KB.ask(cl1)
            expanded = cl2 in KB.clauses

            if safe and not expanded:
                safe_list.append(p)

            cl3 = utils.expr("S({})".format(room))
            s = cl3 in KB.clauses
            if s:
                s_list.append(p)

    return safe_list, s_list


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


def KB_tell_WUM_PIT_ADJ_SAFE(KB, size, pnt, cur_room):
    if in_map(size, pnt):
        # Check corner or edge
        KB_tell_corner_edge(KB, size, pnt)
        # Add Adjacent fact
        room = point_to_room(pnt, size).to_string()
        adj = utils.expr("ADJ({}, {})".format(cur_room, room))
        if adj not in KB.clauses:
            KB.tell(adj)
        wum, pit, safe = KB_asking(KB, room)
        #print(room, "Safe", not not safe)
        if wum:
            cl = utils.expr("WUM({})".format(room))
            if cl not in KB.clauses:
                KB.tell(cl)
        if pit:
            cl = utils.expr("PIT({})".format(room))
            if cl not in KB.clauses:
                KB.tell(cl)
        if safe:
            cl = utils.expr("SAFE({})".format(room))
            if cl not in KB.clauses:
                KB.tell(cl)


def update_KB(KB, size, pnt):
    up, down, left, right = pnt.adj()
    room = point_to_room(pnt, size).to_string()
    KB_tell_WUM_PIT_ADJ_SAFE(KB, size, up, room)
    KB_tell_WUM_PIT_ADJ_SAFE(KB, size, down, room)
    KB_tell_WUM_PIT_ADJ_SAFE(KB, size, left, room)
    KB_tell_WUM_PIT_ADJ_SAFE(KB, size, right, room)


def think(world, KB, cur: Point, map):

    update_KB(KB, world.map_size, cur)
    #print("KB",KB.clauses)
    sal, sl = find_safe(world, KB)

    if not sal and not sl:
        act = ["Go_Home"]
    elif sal:
        #print("found safe")
        #print(sal)
        for p in sal:
            map[p.x][p.y] = True
        act = ["Move"]
        sal.sort(key=lambda x: cur.manhattan_distance(x))
        goal = sal.pop(0)
        dir = dir_from_path(BFS(map, cur, goal))
        act += dir
    else:
        #print("found B")
        for p in sl:
            map[p.x][p.y] = True
        sl.sort(key=lambda x: sum([1 if in_map(world.map_size,i) and i in sl else 0 for i in x.diag()]))
        act = ["Move"]
        goal = sl.pop()
        dir = dir_from_path(BFS(map, cur, goal))
        act += dir
        act.append("Shoot_arrow")

    return act

