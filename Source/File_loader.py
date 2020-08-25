import os
import random
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
               "BGS": "Breeze_Gold_Stench"}
DEFAULT_NUM = {"W":1,
               "P":3,
               "G":1,
               "Size":5}


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
        if cur_pos.x >= 0 and cur_pos.x < self.map_size and cur_pos.y >= 0 and cur_pos.y < self.map_size:
            return True
        return False

    def is_valid_move(self, cur_pos, direction):
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


def generate_map(input_dir=INPUT_DIR, size:int=DEFAULT_NUM["Size"], now:int=DEFAULT_NUM["W"], nop:int=DEFAULT_NUM["P"], nog:int=DEFAULT_NUM["G"]):
    file_name = input_dir + '\\' + str(size) + "x"+ str(size) + "_" + str(now) + "W" + "_" + str(nop) + "P" + ".txt"
    str_map = [["-" for _ in range(size)] for _ in range(size)]  # generate empty size x size map
    wl = []
    for _ in range(now):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        while (x, y) in wl:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
        wl.append((x, y))
    pl = []
    for _ in range(nop):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        while (x, y) in pl or (x, y) in wl:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
        pl.append((x, y))
    gl = []
    for _ in range(nog):
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        while (x, y) in pl + wl + gl:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
        gl.append((x, y))

    for p in pl:
        blk_rng = range(-1, 2)
        for dx in blk_rng:
            for dy in blk_rng:
                if p[0] + dx not in range(size) or p[1] + dy not in range(size):
                    continue
                str_map[p[0] + dx][p[1] + dy] = "B" if str_map[p[0] + dx][p[1] + dy] in ("-", "B") else str_map[p[0] + dx][p[1] + dy] + "B"
        str_map[p[0]][p[1]] = "P"

    for g in gl:
        str_map[g[0]][g[1]] = "G" if str_map[g[0]][g[1]] in ("-", "G") else str_map[g[0]][g[1]] + "G"

    for w in wl:
        blk_rng = range(-1, 2)
        for dx in blk_rng:
            for dy in blk_rng:
                if w[0] + dx not in range(size) or w[1] + dy not in range(size):
                    continue
                str_map[w[0] + dx][w[1] + dy] = "S" if str_map[w[0] + dx][w[1] + dy] in ("-","S") else str_map[w[0] + dx][w[1] + dy] + "S"
        str_map[w[0]][w[1]] = "W"

    with open(file_name, "w") as fout:
        fout.write(str(size) + "\n")
        for i in range(size):
            for j in range(size):
                end = " " if j + 1 < size else "\n"
                fout.write(str_map[i][j] + end)



if __name__ == "__main__":
    generate_map()
    """input_list = Input()
    input_list.items()
    map = input_list.get_map("input.txt")
    map.print_entities()
    print(map.random_spawning_location())"""
