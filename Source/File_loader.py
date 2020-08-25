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
OBJECT_DICT = { "A": "Agent",
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
        x_pos, y_pos = (0,0)
        while True:
            row_pos = random.randint(0, self.map_size - 1)
            col_pos = random.randint(0, self.map_size - 1)

            if self.map_data[row_pos][col_pos] != "W" and self.map_data[row_pos][col_pos] != "P":
                break
        print(self.map_data[row_pos][col_pos])
        return Point(int(row_pos), int(col_pos))

    def is_in_map(self, cur_pos: Point):
        if cur_pos.x >=0 and cur_pos.x < self.map_size and cur_pos.y >=0 and cur_pos.y < self.map_size:
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



if __name__ == "__main__":
    input_list = Input()
    input_list.items()
    map = input_list.get_map("input.txt")
    map.print_entities()
    print(map.random_spawning_location())
