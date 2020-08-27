import turtle
import time
from File_loader import *
import sys

# ---------------------------------------------------------------
val_x = 300
val_y = 250
PIXEL_SIZE = 70
GOLD = 100
DELAY_TIME = 0.5
DEATH_COST = 10000
width = 1000
height = 800
style = ('Courier', 20, 'italic')
# --------------------------------------------Initial things-----------------------------
window = turtle.Screen()
root = turtle.Screen()._root
root.iconbitmap("..\\Images\\icon\\game.ico")
window.bgcolor('black')
window.title('AI WUMPUS')
window.setup(width, height, startx=0, starty=20)
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
        self.goto((-1) * width / 3, height / 3 + 50)
        # self.write(self.message, font=style, align='left')
        self.hideturtle()

    def writeMessage(self, message=""):
        self.clear()
        self.write(message, font=style, align='left')
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

    def Discover(self):
        if self.explored:
            return
        else:
            if self.obj_type == '-':
                self.shape("..\\Images\\70\\EMPTY.gif")
            elif self.obj_type == 'B' or self.obj_type == 'BW':
                self.shape("..\\Images\\70\\BREEZE.gif")
            elif self.obj_type == 'BS' or self.obj_type == 'BSW':
                self.shape("..\\Images\\70\\BREEZE_STENCH.gif")
            elif self.obj_type == 'BGS' or self.obj_type == 'BGSW':
                self.shape("..\\Images\\70\\BREEZE_GOLD_STENCH.gif")
                # self.shape("..\\Images\\70\\BREEZE_GOLD_STENCH.gif")
            elif self.obj_type == 'W':
                self.shape("..\\Images\\70\\WUMPUS.gif")
            elif self.obj_type == 'S':
                self.shape("..\\Images\\70\\STENCH.gif")
            elif self.obj_type == 'GS' or self.obj_type =='GSW':
                self.shape("..\\Images\\70\\GOLD_STENCH.gif")
                # self.shape("..\\Images\\70\\GOLD_STENCH.gif")
            elif self.obj_type == 'BG' or self.obj_type == 'BGW':
                self.shape("..\\Images\\70\\BREEZE_GOLD.gif")
                # self.shape("..\\Images\\70\\BREEZE_GOLD.gif")
            elif self.obj_type == 'G' or self.obj_type == 'GW':
                self.shape("..\\Images\\70\\GOLD.gif")
                # self.shape("..\\Images\\70\\GOLD.gif")
            elif self.obj_type == 'P':
                self.shape("..\\Images\\70\\PIT.gif")

    def reveal_wumpus(self):
        self.shape("..\\Images\\70\\WUMPUS.gif")
        #self.showturtle()
        #self.forward(0)

    def reveal_pit(self):
        self.shape("..\\Images\\70\\PIT.gif")
        #self.showturtle()
        #self.forward(0)


class Player(turtle.Turtle):
    def __init__(self, init_pos: Point = None):
        turtle.Turtle.__init__(self)
        self.position = init_pos if init_pos else Point()
        self.shape("..\\Images\\70\\RIGHT.gif")
        self.color('green')
        self.penup()
        self.speed(0)
        self.gold = 0

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
    """
    def check_status(self, other: Room):
        if other.obj_type != 'W' and other.obj_type != 'P':
            return False
        else:
            return (self.xcor() == other.xcor()) and (self.ycor() == other.ycor())
    """

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
            """
            if item == "P":
                pit_location_list.append(Point(i,j))
            elif item == "W":
                wumpus_location_list.append(Point(i,j))
            """

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

    room_item = data.OBJECT_DICT[data.map_data[player.position.x][player.position.y]]
    message = "Current pos: (" + str(data.map_size - player.position.x - 1) + ", " + str(
        player.position.y) + ") - Found " + room_item
    mes.writeMessage(message)
    while not died and not quit:
        # Time delay
        time.sleep(DELAY_TIME)

        # Check valid move

        next_action = random.choice(["Move"])#, "Shoot_arrow"
        if next_action == "Move":
            step += 1
            room_map[player.position.x][player.position.y].showturtle()

            dir = ["Up", "Down", "Left", "Right"]
            pl_x = player.position.x
            pl_y = player.position.y
            while dir:
                player_dir = random.choice(dir)
                dir.remove(player_dir)
                if data.is_valid_move(player.position, player_dir):
                    player.move(player_dir)
                    break

            room_map[pl_x][pl_y].Discover()
            room_map[pl_x][pl_y].hideturtle()

            room_item = data.map_data[pl_x][pl_y]
            message = "Current pos: (" + str(data.map_size - pl_x - 1) + ", " + str(
                pl_y) + ") - Found " + data.OBJECT_DICT[room_item]
            mes.writeMessage(message)
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
                player.gold += GOLD
                print("Player found gold!")
                data.map_data[pl_x][pl_y] = data.map_data[pl_x][pl_y].replace("G","")
                data.map_data[pl_x][pl_y] += "-" if not map.map_data[pl_x][pl_y] else ""
            else:
                pass

        elif next_action == "Shoot_arrow":
            dir = ["Up", "Down", "LEFT", "Right"]

            shoot_dir = random.choice(dir)
            if data.player_shoot(player.position, shoot_dir):
                print("Player killed a wumpus in this room")
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
    map = input_list.get_map("input.txt")
    # map.print_entities()
    init_pos = map.random_spawning_location()
    # messagebox.showinfo("UI will started!!","Click ok to start!!!")
    startGame(map, init_pos)
