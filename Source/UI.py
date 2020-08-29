import turtle
import time
from File_loader import *
import sys
from wumpus_data_world import *
from path_search import BFS, dir_from_path
# ---------------------------------Front-end stuff------------------------
val_x = 300
val_y = 270
PIXEL_SIZE = 70
width = 1000
height = 820
DELAY_TIME = 0.2
style = ('Courier', 20, 'italic')
# --------------------------------------COST FOR SCORING---------------------------
GOLD = 100
ARROW_COST = 100
DEATH_COST = 10000
STEP_COST = 10
EXIT_MAP = 10
MAX_STAMINA = 10000000 * STEP_COST
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
          "..\\Images\\70\\UNKNOWN.gif",
          "..\\Images\\70\\ESCAPE.gif"]
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
        self.write("Current pos: " + message, font=style, align='left')
        self.goto((-1) * width / 3, height / 3 + 60)
        self.write("Score: " + str(score) + "\t\tGold found: " + str(gold_found), font=style, align='left')
        self.goto((-1) * width / 3, height / 3 + 30)
        self.write("Steps: " + str(step), font=style, align='left')
        self.hideturtle()

    def tracePathMessage(self, cur_pos:str, goal_pos:str, step: int):
        self.clear()
        self.goto((-1) * width / 3, height / 3 + 90)
        self.write("Player is tracing back to initial pos at "+ goal_pos, font=style, align='left')
        self.goto((-1) * width / 3, height / 3 + 60)
        self.write("Current pos: " + cur_pos, font=style, align='left')
        self.goto((-1) * width / 3, height / 3 + 30)
        self.write("Steps: " + str(step), font=style, align='left')
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

    def Refresh(self, obj_type='-', explored=False, hidden = False):
        self.obj_type = obj_type
        self.explored = explored
        if not hidden:
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
            elif self.obj_type == 'ESC':
                self.shape("..\\Images\\70\\ESCAPE.gif")

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
        self.stamina = MAX_STAMINA

    def go_up(self):
        print("Player go up")
        move_to_x = self.xcor()
        move_to_y = self.ycor() + PIXEL_SIZE
        self.shape("..\\Images\\70\\UP.gif")
        self.goto(move_to_x, move_to_y)
        self.forward(0)
        self.position.x -= 1

    def go_down(self):
        print("Player go down")
        move_to_x = self.xcor()
        move_to_y = self.ycor() - PIXEL_SIZE
        self.shape("..\\Images\\70\\DOWN.gif")
        self.goto(move_to_x, move_to_y)
        self.forward(0)
        self.position.x += 1

    def go_left(self):
        print("Player go left")
        move_to_x = self.xcor() - PIXEL_SIZE
        move_to_y = self.ycor()
        self.shape("..\\Images\\70\\LEFT.gif")
        self.goto(move_to_x, move_to_y)
        self.forward(0)
        self.position.y -= 1

    def go_right(self):
        print("Player go right")
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


def startGame(data: Map, init_pos: Point):
    step = 1
    setup_map(data.map_data, init_pos.clone())
    """
    turtle.listen()
    turtle.onkey(player.go_up, 'Up')
    turtle.onkey(player.go_down, 'Down')
    turtle.onkey(player.go_right, 'Right')
    turtle.onkey(player.go_left, 'Left')
    """
    died = False
    quit = False
    path_map = [[False] * data.map_size for _ in range(data.map_size)]

    pl_x = player.position.x
    pl_y = player.position.y
    room_map[pl_x][pl_y].hideturtle()
    room_map[pl_x][pl_y].Discover()
    path_map[pl_x][pl_y] = True
    room_item = data.map_data[pl_x][pl_y]
    message = str(point_to_room(player.position, data.map_size).coordinate()) + "\tFound " + \
              data.OBJECT_DICT[room_item]
    mes.writeMessage(message, player.score, step, player.gold_found)
    # init pos check

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

    # ---------------------------------game loop -----------------------------------
    while not died and not quit and player.stamina > 0:
        # Time delay
        time.sleep(DELAY_TIME)
        # print(KB.clauses)
        # Check valid move
        room = point_to_room(player.position, data.map_size)
        room_sym = room.to_string()

        room_item = data.map_data[player.position.x][player.position.y]

        #print("FFFFFFFFFFF", room_item)
        if room_item in ['-', 'G']:
            cl = utils.expr("NULL({})".format(room_sym))
            if cl not in KB.clauses:
                KB.tell(cl)
        if 'B' in room_item:
            cl = utils.expr("B({})".format(room_sym))
            if cl not in KB.clauses:
                KB.tell(cl)

        if 'S' in room_item:
            cl = utils.expr("S({})".format(room_sym))
            if cl not in KB.clauses:
                KB.tell(cl)
        cl = utils.expr("EXP({})".format(room_sym))
        if cl not in KB.clauses:
            KB.tell(cl)
        print("at",room_sym, "found",room_item)
        print(KB.clauses)
        next_action = think(map, KB, player.position, path_map)
        # , "Shoot_arrow"
        print("From KB: ", next_action)
        if "Move" in next_action:
            shoot_af = "Shoot_arrow" in next_action
            if shoot_af:
                next_action.remove("Shoot_arrow")
            next_action.remove("Move")
            while next_action:
                player_dir = next_action.pop(0)
                if data.is_valid_move(player.position, player_dir):
                    room_map[player.position.x][player.position.y].showturtle()
                    step += 1
                    player.score -= STEP_COST
                    player.stamina -= STEP_COST
                    player.move(player_dir)

                pl_x = player.position.x
                pl_y = player.position.y
                room_map[pl_x][pl_y].hideturtle()
                room_map[pl_x][pl_y].Discover()
                window.update()
                path_map[pl_x][pl_y] = True
                room_item = data.map_data[pl_x][pl_y]
                message = str(point_to_room(player.position, data.map_size).coordinate()) + "\tFound " + \
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
                    break

                elif "W" in room_item:
                    print("Player got eaten by the wumpus!!")
                    player.destroy()
                    room_map[pl_x][pl_y].reveal_wumpus()
                    room_map[pl_x][pl_y].showturtle()
                    window.update()
                    time.sleep(2)
                    died = True
                    break

                elif "G" in room_item:
                    player.score += GOLD
                    player.gold_found += 1
                    player.stamina = MAX_STAMINA
                    print("Player found gold!")
                    data.map_data[pl_x][pl_y] = data.map_data[pl_x][pl_y].replace("G", "")
                    data.map_data[pl_x][pl_y] += "-" if not map.map_data[pl_x][pl_y] else ""
                    room_map[pl_x][pl_y].obj_type = data.map_data[pl_x][pl_y]
                else:
                    pass
                time.sleep(DELAY_TIME)
                window.update()
            if shoot_af:
                next_action.append("Shoot_arrow")
        print(next_action)
        if "Shoot_arrow" in next_action:
            print(next_action)
            next_action.remove("Shoot_arrow")
            next_action = ["Up", "Down", "Left", "Right"]
            while next_action:
                shoot_dir = random.choice(next_action)
                next_action.remove(shoot_dir)

                if not data.player_shoot(player.position, shoot_dir):
                    print("Player wasted an arrow")
                else:
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
                        if "S" not in data.map_data[w_pos_up.x][w_pos_up.y]:
                            room_up = point_to_room(w_pos_up, data.map_size)
                            room_sym_up = room_up.to_string()
                            cl = utils.expr("EXP({})".format(room_sym_up))
                            if cl in KB.clauses:
                                room_map[w_pos_up.x][w_pos_up.y].Refresh(data.map_data[w_pos_up.x][w_pos_up.y], False, False)
                                cl_up = utils.expr("S({})".format(room_sym_up))
                                #print("+++++++++++++++++++++++",cl_up)
                                KB.retract(cl_up)
                                KB.retract(cl)
                            else:
                                room_map[w_pos_up.x][w_pos_up.y].Refresh(data.map_data[w_pos_up.x][w_pos_up.y], False, True)

                    if data.is_in_map(w_pos_down):
                        if "S" not in data.map_data[w_pos_down.x][w_pos_down.y]:
                            room_down = point_to_room(w_pos_down, data.map_size)
                            room_sym_down = room_down.to_string()
                            cl = utils.expr("EXP({})".format(room_sym_down))
                            if cl in KB.clauses:
                                room_map[w_pos_down.x][w_pos_down.y].Refresh(data.map_data[w_pos_down.x][w_pos_down.y],False, False)
                                cl_down = utils.expr("S({})".format(room_sym_down))
                                #print("+++++++++++++++++++++++",cl_down)
                                KB.retract(cl_down)
                                KB.retract(cl)
                            else:
                                room_map[w_pos_down.x][w_pos_down.y].Refresh(data.map_data[w_pos_down.x][w_pos_down.y],False, True)

                    if data.is_in_map(w_pos_left):
                        if "S" not in data.map_data[w_pos_left.x][w_pos_left.y]:
                            room_left = point_to_room(w_pos_left, data.map_size)
                            room_sym_left = room_left.to_string()
                            cl = utils.expr("EXP({})".format(room_sym_left))
                            if cl in KB.clauses:
                                room_map[w_pos_left.x][w_pos_left.y].Refresh(data.map_data[w_pos_left.x][w_pos_left.y], False, False)
                                cl_left = utils.expr("S({})".format(room_sym_left))
                                #print("+++++++++++++++++++++++",cl_left)
                                KB.retract(cl_left)
                                KB.retract(cl)
                            else:
                                room_map[w_pos_left.x][w_pos_left.y].Refresh(data.map_data[w_pos_left.x][w_pos_left.y], False, True)

                    if data.is_in_map(w_pos_right):
                        if "S" not in data.map_data[w_pos_right.x][w_pos_right.y]:
                            room_right = point_to_room(w_pos_right, data.map_size)
                            room_sym_right = room_right.to_string()
                            cl = utils.expr("EXP({})".format(room_sym_right))
                            if cl in KB.clauses:
                                room_map[w_pos_right.x][w_pos_right.y].Refresh(data.map_data[w_pos_right.x][w_pos_right.y], False, False)
                                cl_right = utils.expr("S({})".format(room_sym_right))
                                #print("+++++++++++++++++++++++",cl_right)
                                KB.retract(cl_right)
                                KB.retract(cl)
                            else:
                                room_map[w_pos_right.x][w_pos_right.y].Refresh(data.map_data[w_pos_right.x][w_pos_right.y], False, False)

                    break

        elif "Go_Home" in next_action:
            quit = True
        window.update()

    #Escape to initial pos to exit game
    #print(path_map)
    #time.sleep(20)
    if not died:
        path_list = BFS(path_map, player.position, init_pos)
        guide_list = dir_from_path(path_list)
        room_map[init_pos.x][init_pos.y].Refresh("ESC", False)
        window.update()
        if not guide_list:
            print("Luckily, the player is already at exit pos", player.position.coordinate(), init_pos.coordinate())
        else:
            while guide_list:
                step += 1
                time.sleep(DELAY_TIME)
                room_map[player.position.x][player.position.y].showturtle()
                player.move(guide_list.pop(0))
                room_map[player.position.x][player.position.y].hideturtle()
                room_map[player.position.x][player.position.y].Discover()
                mes.tracePathMessage(str(point_to_room(player.position, data.map_size).coordinate()),str(point_to_room(init_pos, data.map_size).coordinate()), step)

                window.update()

            time.sleep(3)


    print("END game:")
    # turtle.exitonclick()
    endGame()


if __name__ == "__main__":
    input_list = Input()
    input_list.items()
    map = input_list.get_map("8x8_1G_1W_10P.txt")
    # map.print_entities()
    init_pos = map.random_spawning_location()
    # messagebox.showinfo("UI will started!!","Click ok to start!!!")
    startGame(map, Point(0, 3))
