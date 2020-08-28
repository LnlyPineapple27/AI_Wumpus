import os
import random

from typing import List

from Point import Point

# import glob
# from UI import startGame
"""
STENCH_BREEZE = "BS"
GOLD = "G"
STENCH = "S"
BREEZE = "B"
WUMPUS = "W"
PIT = "P"
EMPTY = "-"
"""
INPUT_DIR = "..\\Input"
OBJECT_DICT = {"A": "Agent",
               "-": "Empty",
               "B": "Breeze",
               "S": "Stench",
               "P": "Pit",
               "W": "Wumpus",
               "G": "Gold",
               "BS": "Breeze_Stench",
               "GS": "Gold_Stench",
               "BG": "Breeze_Gold",
               "BGS": "Breeze_Gold_Stench",
               "SW": "Stench_Wumpus",
               "BW": "Breeze_Wumpus",
               "GW": "Gold_Wumpus",
               "BSW": "Breeze_Stench_Wumpus",
               "BGW":"Breeze_Gold_Wumpus",
               "GSW": "Gold_Stench_Wumpus",
               "BGSW": "Breeze_Gold_Stench_Wumpus"}
DEFAULT_NUM = {"W": 1,
               "P": 1,
               "G": 10,
               "Size": 6}
SYM = ["A", "W", "P"]
SIG = ["B", "S", "G", "-"]


class Map:
    def __init__(self, size=0, map_data=None):
        self.OBJECT_DICT = OBJECT_DICT
        self.map_size = size
        self.map_data = map_data

    def print_raw_data(self):
        for i in self.map_data:
            print(i)

    def print_entities(self) -> None:
        for row in self.map_data:
            for obj in row:
                print(self.OBJECT_DICT[obj], end="\t")
            print("\n")

    def random_spawning_location(self):
        x_pos, y_pos = (0, 0)
        while True:
            row_pos = random.randint(0, self.map_size - 1)
            col_pos = random.randint(0, self.map_size - 1)

            if self.map_data[row_pos][col_pos] != "W" and self.map_data[row_pos][col_pos] != "P":
                break
        print(self.map_data[row_pos][col_pos])
        return Point(int(row_pos), int(col_pos))

    def is_in_map(self, cur_pos: Point):
        if 0 <= cur_pos.x < self.map_size and 0 <= cur_pos.y < self.map_size:
            return True
        return False

    def is_valid_move(self, cur_pos: Point, direction):
        if direction == "Up":
            return self.is_in_map(cur_pos.up())
        elif direction == "Down":
            return self.is_in_map(cur_pos.down())
        elif direction == "Left":
            return self.is_in_map(cur_pos.left())
        elif direction == "Right":
            return self.is_in_map(cur_pos.right())
        else:
            return False

    def have_wumpus(self, room_pos: Point):
        if not self.is_in_map(room_pos):
            return False
        elif "W" in self.map_data[room_pos.x][room_pos.y]:
            return True
        else:
            return False

    def have_wumpus_nearby(self, room_pos: Point):
        if self.have_wumpus(room_pos.up()):
            return True
        if self.have_wumpus(room_pos.down()):
            return True
        if self.have_wumpus(room_pos.left()):
            return True
        if self.have_wumpus(room_pos.right()):
            return True
        return False

    def remove_stench(self, room_pos):
        if self.is_in_map(room_pos):
            if not self.have_wumpus_nearby(room_pos):
                room_item = self.map_data[room_pos.x][room_pos.y]
                self.map_data[room_pos.x][room_pos.y] = room_item.replace('S', '')
                self.map_data[room_pos.x][room_pos.y] += "-" if not self.map_data[room_pos.x][room_pos.y]else ""

    def remove_stench_after_wumpus_is_killed(self, wumpus_pos: Point):
        self.remove_stench(wumpus_pos.up())
        self.remove_stench(wumpus_pos.down())
        self.remove_stench(wumpus_pos.right())
        self.remove_stench(wumpus_pos.left())

    def wumpus_got_killed(self, wumpus_pos: Point):
        room_item = self.map_data[wumpus_pos.x][wumpus_pos.y]
        if "W" in room_item:
            self.map_data[wumpus_pos.x][wumpus_pos.y] = room_item.replace('W', '')
            self.map_data[wumpus_pos.x][wumpus_pos.y] += "-" if not self.map_data[wumpus_pos.x][wumpus_pos.y]else ""
            self.remove_stench_after_wumpus_is_killed(wumpus_pos)
            return True
        else:
            return False

    def player_shoot(self, cur_pos: Point, direction):
        if direction == "Up":
            if self.is_in_map(cur_pos.up()):
                return self.wumpus_got_killed(cur_pos.up())
        elif direction == "Down":
            if self.is_in_map(cur_pos.down()):
                return self.wumpus_got_killed(cur_pos.down())
        elif direction == "Left":
            if self.is_in_map(cur_pos.left()):
                return self.wumpus_got_killed(cur_pos.left())
        elif direction == "Right":
            if self.is_in_map(cur_pos.right()):
                return self.wumpus_got_killed(cur_pos.right())
        return False


class Input:
    def __init__(self, input_dir=INPUT_DIR):
        self.path_list = {}
        with os.scandir(input_dir) as i:
            for entry in i:
                if entry.is_file():
                    self.path_list[entry.name] = input_dir + '\\' + entry.name

    def items(self) -> None:
        print("Item\t\t-\tPath")

        for item in self.path_list.items():
            print(item[0] + "\t-\t" + item[1])

    def get_map(self, file_name: str = None) -> Map:
        file_path = self.path_list[file_name] if file_name and file_name in self.path_list.keys() \
            else random.choices(list(self.path_list.values())).pop()

        with open(file_path, 'r') as file:
            lines = file.readlines()
            # get size of map
            size = int(lines.pop(0))
            map_data = list()

            for i in range(size):
                # Input items are separated by '.'
                row_list = lines[i].rstrip('\n').split(".")
                map_data.append([row_list[item] for item in range(size)])
        return Map(size, map_data)


def generate_point(nop: int = 1, sos: int = 1, invl: list = None) -> list:
    """
    Generate points\n
    :param nop: Number of points
    :param sos: Size of space
    :param invl: Invalid list (Don't generate to here)
    :return:  List of point
    """
    if not invl:
        invl = []
    pl = []  # Init points list
    for _ in range(nop):
        p = Point()
        p.rand(sos)
        while p in pl or p in invl:
            p.rand(sos)
        pl.append(p)
    return pl


def add_entity(mat, sym, sign, lop):
    """
    Add entities with symbol and sign\n
    :param mat: Matrix
    :param sym: Symbol of entity
    :param sign: Sign of entity
    :param lop: List entity's points
    :return: Matrix with entities added
    """
    is_empty = lambda p: mat[p.x][p.y] == "-"
    is_in_map = lambda p: 0 <= p.x < len(mat) and 0 <= p.y < len(mat)
    is_entity = lambda p: mat[p.x][p.y] in SYM
    for pnt in lop:
        if sign:
            u, d, l, r = pnt.up(), pnt.down(), pnt.left(), pnt.right()
            if is_in_map(u) and not is_entity(u):
                u = u
                if is_empty(u):
                    mat[u.x][u.y] = sign
                else:
                    mat[u.x][u.y] += sign if sign not in mat[u.x][u.y] else ""
            if is_in_map(d) and not is_entity(d):
                d = d
                if is_empty(d):
                    mat[d.x][d.y] = sign
                else:
                    mat[d.x][d.y] += sign if sign not in mat[d.x][d.y] else ""
            if is_in_map(l) and not is_entity(l):
                if is_empty(l):
                    mat[l.x][l.y] = sign
                else:
                    mat[l.x][l.y] += sign if sign not in mat[l.x][l.y] else ""
            if is_in_map(r) and not is_entity(r):
                if is_empty(r):
                    mat[r.x][r.y] = sign
                else:
                    mat[r.x][r.y] += sign if sign not in mat[r.x][r.y] else ""
        if sym == "G" or sym == "W":
            mat[pnt.x][pnt.y] = sym if is_empty(pnt) else mat[pnt.x][pnt.y] + sym
        else:
            mat[pnt.x][pnt.y] = sym
    return mat


def create_entities_matrix(size=DEFAULT_NUM["Size"], now=DEFAULT_NUM["W"], nop=DEFAULT_NUM["P"], nog=DEFAULT_NUM["G"]):
    """
    Create entities matrix\n
    :param size: Size of map
    :param now: Number of wumpuses
    :param nop: Number of pits
    :param nog: Number of golds
    :return: None
    """
    mat = [["-" for _ in range(size)] for _ in range(size)]  # generate empty size x size map
    wl = generate_point(now, size - 1, None)
    pl = generate_point(nop, size - 1, wl)
    gl = generate_point(nog, size - 1, pl)
    mat = add_entity(mat, "P", "B", pl)
    mat = add_entity(mat, "G", None, gl)
    mat = add_entity(mat, "W", "S", wl)
    return mat


def generate_map(input_dir=INPUT_DIR, size=DEFAULT_NUM["Size"], now=DEFAULT_NUM["W"], nop=DEFAULT_NUM["P"],
                 nog=DEFAULT_NUM["G"]) -> None:
    """
    Generate a wumpus map to <size>_<Number of gold>_<Number of wumpus>_<Number of pit>.txt file\n
    :param input_dir: Input directory
    :param size: Size of map
    :param now: Number of wumpuses
    :param nop: Number of pits
    :param nog: Number of golds
    :return: None
    """
    file_name = input_dir + '\\' + str(size) + "x" + str(size) + "_"
    file_name += str(nog) + "G_" + str(now) + "W_" + str(nop) + "P.txt"
    matrix = create_entities_matrix(size, now, nop, nog)
    with open(file_name, "w") as fout:
        fout.write(str(size) + "\n")
        for i in range(size):
            for j in range(size):
                end = "." if j + 1 < size else "\n"
                fout.write(matrix[i][j] + end)


if __name__ == "__main__":
    generate_map()
    """
    input_list = Input()
    input_list.items()
    map = input_list.get_map("8x8_10G_10W_10P.txt")
    map.print_entities()
    print(map.random_spawning_location())
    """
