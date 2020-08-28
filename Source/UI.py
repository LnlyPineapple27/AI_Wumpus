import turtle
import time
from File_loader import *
import sys
from wumpus_data_world import *

# ---------------------------------Front-end stuff------------------------
val_x = 300
val_y = 270
PIXEL_SIZE = 70
width = 1000
height = 820
DELAY_TIME = 0.7
style = ('Courier', 20, 'italic')
# --------------------------------------COST FOR SCORING---------------------------
GOLD = 100
ARROW_COST = 100
DEATH_COST = 10000
STEP_COST = 10
EXIT_MAP = 10
# --------------------------------------------Initial things-----------------------------
window = turtle.Screen()
root = turtle.Screen()._root
root.iconbitmap("..\\Images\\icon\\game.ico")
window.bgcolor('black')
window.title('AI WUMPUS')
window.setup(width, height, startx=0, starty=10)
window.tracer(0)

images = ["..\\Images\\70\\DOWN.gif",
          "..\\Images\\70\\LEFT.gif",
          "..\\Images\\70\\RIGHT.gif",
          "..\\Images\\70\\UP.gif",
          "..\\Images\\70\\WUMPUS.gif",
          "..\\Images\\70\\BREEZE.gif",
          "..\\Images\\70\\BREEZE_GOLD.gif",
          "..\\Images\\70\\BREEZE_STENCH.gif",
          "..\\Images\\70\\BREEZE_GOLD_STENCH.gif",
          "..\\Images\\70\\GOLD.gif",
          "..\\Images\\70\\GOLD_STENCH.gif",
          "..\\Images\\70\\PIT.gif",
          "..\\Images\\70\\EMPTY.gif",
          "..\\Images\\70\\STENCH.gif",
          "..\\Images\\70\\UNKNOWN.gif"]
KB = init_KB()

for img in images:
    turtle.register_shape(img)


class ScreenMessage(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        # self.shape("Circle")
        # self.message = message
        self.color('yellow')
        self.penup()
        self.speed(0)
        self.goto((-1) * width / 3, height / 3 + 90)
        self.write("Welcome, HUNTER!!!!", font=style, align='left')
        self.hideturtle()
        time.sleep(1)

    def writeMessage(self, message: str = "", score: int = -1, step: int = 0, gold_found: int = 0):
        self.clear()
        self.goto((-1) * width / 3, height / 3 + 90)
        self.write(message, font=style, align='left')
        self.goto((-1) * width / 3, height / 3 + 60)
        self.write("Score: " + str(score) + "\t\tGold found: " + str(gold_found), font=style, align='left')
        self.goto((-1) * width / 3, height / 3 + 30)
        self.write("Step: " + str(step), font=style, align='left')
        self.hideturtle()


class Room(turtle.Turtle):
    def __init__(self, x=0, y=0, obj_type='-', explored=False):
        turtle.Turtle.__init__(self)
        self.shape("..\\Images\\70\\UNKNOWN.gif")
        self.color('blue')
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.obj_type = obj_type
        self.explored = explored

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def Refresh(self, obj_type='-', explored=False):
        self.obj_type = obj_type
        self.explored = explored
        self.Discover()

    def Discover(self):
        if self.explored:
            return
        else:
            self.explored = True
            if self.obj_type == '-':
                self.shape("..\\Images\\70\\EMPTY.gif")
            elif self.obj_type == 'B' or self.obj_type == 'BW':
                self.shape("..\\Images\\70\\BREEZE.gif")
            elif self.obj_type == 'BS' or self.obj_type == 'BSW':
                self.shape("..\\Images\\70\\BREEZE_STENCH.gif")
            elif self.obj_type == 'BGS' or self.obj_type == 'BGSW':
                self.shape("..\\Images\\70\\BREEZE_STENCH.gif")
                # self.shape("..\\Images\\70\\BREEZE_GOLD_STENCH.gif")
            elif self.obj_type == 'W':
                self.shape("..\\Images\\70\\EMPTY.gif")
            elif self.obj_type == 'S':
                self.shape("..\\Images\\70\\STENCH.gif")
            elif self.obj_type == 'GS' or self.obj_type == 'GSW':
                self.shape("..\\Images\\70\\STENCH.gif")
                # self.shape("..\\Images\\70\\GOLD_STENCH.gif")
            elif self.obj_type == 'BG' or self.obj_type == 'BGW':
                self.shape("..\\Images\\70\\BREEZE.gif")
                # self.shape("..\\Images\\70\\BREEZE_GOLD.gif")
            elif self.obj_type == 'G' or self.obj_type == 'GW':
                self.shape("..\\Images\\70\\EMPTY.gif")
                # self.shape("..\\Images\\70\\GOLD.gif")
            elif self.obj_type == 'P':
                self.shape("..\\Images\\70\\PIT.gif")

    def reveal_wumpus(self):
        self.shape("..\\Images\\70\\WUMPUS.gif")
        # self.showturtle()
        # self.forward(0)

    def reveal_pit(self):
        self.shape("..\\Images\\70\\PIT.gif")
        # self.showturtle()
        # self.forward(0)
"""
    def remove_stench(self):
        t_shape = self.shape()
        if t_shape == "..\\Images\\70\\STENCH.gif":
            self.shape("..\\Images\\70\\EMPTY.gif")
        elif t_shape == "..\\Images\\70\\BREEZE_STENCH.gif":
            self.shape("..\\Images\\70\\BREEZE.gif")
"""

class Player(turtle.Turtle):
    def __init__(self, init_pos: Point = None):
        turtle.Turtle.__init__(self)
        self.position = init_pos if init_pos else Point()
        self.shape("..\\Images\\70\\RIGHT.gif")
        self.color('green')
        self.penup()
        self.speed(0)
        self.score = 0
        self.gold_found = 0

    def go_up(self):
        # print("Player go up")
        move_to_x = self.xcor()
        move_to_y = self.ycor() + PIXEL_SIZE
        self.shape("..\\Images\\70\\UP.gif")
        self.goto(move_to_x, move_to_y)
        self.forward(0)
        self.position.x -= 1

    def go_down(self):
        # print("Player go down")
        move_to_x = self.xcor()
        move_to_y = self.ycor() - PIXEL_SIZE
        self.shape("..\\Images\\70\\DOWN.gif")
        self.goto(move_to_x, move_to_y)
        self.forward(0)
        self.position.x += 1

    def go_left(self):
        # print("Player go left")
        move_to_x = self.xcor() - PIXEL_SIZE
        move_to_y = self.ycor()
        self.shape("..\\Images\\70\\LEFT.gif")
        self.goto(move_to_x, move_to_y)
        self.forward(0)
        self.position.y -= 1

    def go_right(self):
        # print("Player go right")
        move_to_x = self.xcor() + PIXEL_SIZE
        move_to_y = self.ycor()
        self.shape("..\\Images\\70\\RIGHT.gif")
        self.goto(move_to_x, move_to_y)
        self.forward(0)
        self.position.y += 1

    def move(self, next_move: str = None):
        if next_move == "Up":
            self.go_up()
        elif next_move == "Down":
            self.go_down()
        elif next_move == "Left":
            self.go_left()
        elif next_move == "Right":
            self.go_right()
        else:
            pass

    def exit(self):
        self.goto(self.xcor(), self.ycor())

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


# Global variable
player = Player()
mes = ScreenMessage()
room_map = []


# pit_location_list = []
# wumpus_location_list = []

# start position of character
def setup_map(board, init_index):
    player.position = init_index
    print("[Player's initial position]:", player.position.coordinate())
    # 288

    for i in range(len(board)):
        row_map = []
        for j in range(len(board[i])):
            # get the character of each x,y coord
            item = board[i][j]
            screen_x = ((-1) * val_x) + (j * PIXEL_SIZE)
            screen_y = val_y - (i * PIXEL_SIZE)

            row_map.append(Room(screen_x, screen_y, item, False))
        room_map.append(row_map)
    # print Player according to its given location
    room_map[player.position.x][player.position.y].Discover()
    room_map[player.position.x][player.position.y].hideturtle()
    player.goto(((-1) * val_x) + (player.position.y * PIXEL_SIZE), val_y - (player.position.x * PIXEL_SIZE))

    window.update()


def endGame():
    print("[Game closed]")
    sys.exit()


def startGame(data: Map, init_pos):
    step = 1
    setup_map(data.map_data, init_pos)
    """
    turtle.listen()
    turtle.onkey(player.go_up, 'Up')
    turtle.onkey(player.go_down, 'Down')
    turtle.onkey(player.go_right, 'Right')
    turtle.onkey(player.go_left, 'Left')
    """
    died = False
    quit = False

    pl_x = player.position.x
    pl_y = player.position.y
    room_map[pl_x][pl_y].hideturtle()
    room_map[pl_x][pl_y].Discover()
    room_item = data.map_data[pl_x][pl_y]
    message = "Current pos: " + str(point_to_room(player.position, data.map_size).coordinate()) + "\tFound " + \
              data.OBJECT_DICT[room_item]
    mes.writeMessage(message, player.score, step, player.gold_found)
    # check player is dead or not

    if "P" in room_item:
        print("Player fell into a pit!!")
        player.destroy()
        room_map[pl_x][pl_y].reveal_pit()
        room_map[pl_x][pl_y].showturtle()
        window.update()
        time.sleep(2)
        died = True

    elif "W" in room_item:
        print("Player got eaten by the wumpus!!")
        player.destroy()
        room_map[pl_x][pl_y].reveal_wumpus()
        room_map[pl_x][pl_y].showturtle()
        window.update()
        time.sleep(2)
        died = True

    elif "G" in room_item:
        player.score += GOLD
        player.gold_found += 1
        print("Player found gold!")
        data.map_data[pl_x][pl_y] = data.map_data[pl_x][pl_y].replace("G", "")
        data.map_data[pl_x][pl_y] += "-" if not map.map_data[pl_x][pl_y] else ""
        room_map[pl_x][pl_y].obj_type = data.map_data[pl_x][pl_y]
    while not died and not quit:
        # Time delay
        time.sleep(DELAY_TIME)
        # print(KB.clauses)
        # Check valid move
        room = point_to_room(player.position, data.map_size)
        room_sym = room.to_string()
        if '-' in room_item:
            cl = utils.expr("NULL({})".format(room_sym))
            if cl not in KB.clauses:
                KB.tell(cl)
        if 'B' in room_item:
            cls = [utils.expr("B({})".format(room_sym))]
            pit = KB.ask(utils.expr("PIT({})".format(room_sym)))
            if pit:
                cls.append(utils.expr("PIT({})".format(room_sym)))
            for cl in cls:
                if cl not in KB.clauses:
                    KB.tell(cl)
        if 'S' in room_item:
            cls = [utils.expr("S({})".format(room_sym))]
            wum = KB.ask(utils.expr("WUM({})".format(room_sym)))
            if wum:
                cls.append(utils.expr("WUM({})".format(room_sym)))
            for cl in cls:
                if cl not in KB.clauses:
                    KB.tell(cl)
        cl = utils.expr("EXP({})".format(room_sym))
        if cl not in KB.clauses:
            KB.tell(cl)
        print(KB.clauses)
        next_action = random.choice(["Move"])  # , "Shoot_arrow"

        if next_action == "Move":
            room_map[player.position.x][player.position.y].showturtle()

            dir = think(map, KB, player.position)
            while dir:
                player_dir = random.choice(dir)
                dir.remove(player_dir)
                if data.is_valid_move(player.position, player_dir):
                    step += 1
                    player.score -= STEP_COST
                    player.move(player_dir)
                    break

            pl_x = player.position.x
            pl_y = player.position.y
            room_map[pl_x][pl_y].hideturtle()
            room_map[pl_x][pl_y].Discover()
            room_item = data.map_data[pl_x][pl_y]
            message = "Current pos: " + str(point_to_room(player.position, data.map_size).coordinate()) + "\tFound " + \
                      data.OBJECT_DICT[room_item]
            mes.writeMessage(message, player.score, step, player.gold_found)
            # check player is dead or not

            if "P" in room_item:
                print("Player fell into a pit!!")
                player.destroy()
                room_map[pl_x][pl_y].reveal_pit()
                room_map[pl_x][pl_y].showturtle()
                window.update()
                time.sleep(2)
                died = True

            elif "W" in room_item:
                print("Player got eaten by the wumpus!!")
                player.destroy()
                room_map[pl_x][pl_y].reveal_wumpus()
                room_map[pl_x][pl_y].showturtle()
                window.update()
                time.sleep(2)
                died = True

            elif "G" in room_item:
                player.score += GOLD
                player.gold_found += 1
                print("Player found gold!")
                data.map_data[pl_x][pl_y] = data.map_data[pl_x][pl_y].replace("G", "")
                data.map_data[pl_x][pl_y] += "-" if not map.map_data[pl_x][pl_y] else ""
                room_map[pl_x][pl_y].obj_type = data.map_data[pl_x][pl_y]
            else:
                pass


        elif next_action == "Shoot_arrow":
            dir = ["Up", "Down", "LEFT", "Right"]

            shoot_dir = random.choice(dir)
            if data.player_shoot(player.position, shoot_dir):
                print("Player killed a wumpus in", shoot_dir, "room")
                w_pos = player.position
                if shoot_dir == "Up":
                    w_pos = w_pos.up()
                elif shoot_dir == "Down":
                    w_pos = w_pos.down()
                elif shoot_dir == "Left":
                    w_pos = w_pos.left()
                elif shoot_dir == "Right":
                    w_pos = w_pos.right()

                w_pos_up = w_pos.up()
                w_pos_down = w_pos.down()
                w_pos_left = w_pos.left()
                w_pos_right = w_pos.right()
                # Up remove Stench ADJ rooms in UI after Wumpus is killed
                if data.is_in_map(w_pos_up):
                    room_map[w_pos_up.x][w_pos_up.y].Refresh(data.map_data[w_pos_up.x][w_pos_up.y],False)
                if data.is_in_map(w_pos_down):
                    room_map[w_pos_down.x][w_pos_down.y].Refresh(data.map_data[w_pos_down.x][w_pos_down.y],False)
                if data.is_in_map(w_pos_left):
                    room_map[w_pos_left.x][w_pos_left.y].Refresh(data.map_data[w_pos_left.x][w_pos_left.y],False)
                if data.is_in_map(w_pos_right):
                    room_map[w_pos_right.x][w_pos_right.y].Refresh(data.map_data[w_pos_right.x][w_pos_right.y],False)
            else:
                print("Player wasted an arrow")
        else:
            pass

        window.update()
        # nếu ăn vàng thì mất vàng treen map
        # va chạm = cách so sánh pos pLayer và pos room, xét loại room rồi đánh giá died hay thêm vàng

    print("END game:")
    # turtle.exitonclick()
    endGame()


if __name__ == "__main__":
    input_list = Input()
    input_list.items()
    map = input_list.get_map("10x10_10G_3W_3P.txt")
    # map.print_entities()
    init_pos = map.random_spawning_location()
    # messagebox.showinfo("UI will started!!","Click ok to start!!!")
    startGame(map, init_pos)
