import turtle
from tkinter import messagebox
import time
val_x = 400
val_y = 350
PIXEL_SIZE = 70
# --------------------------------------------Initial things-----------------------------
window = turtle.Screen()
root = turtle.Screen()._root
root.iconbitmap("..\\Images\\icon\\game.ico")
window.bgcolor('black')
window.title('AI WUMPUS')
window.setup([1000,800], startx=0, starty=20)
window.tracer(0)
# --------------------------------------------------
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


class Unknown(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("..\\Images\\70\\UNKNOWN.gif")
        self.color('blue')
        self.penup()
        self.speed(0)


class Empty(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("..\\Images\\70\\EMPTY.gif")
        self.color('purple')
        self.penup()
        self.speed(0)


class Gold(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("..\\Images\\70\\GOLD.gif")
        self.color('gold')
        self.penup()
        self.speed(0)
        self.gold = GOLD
        self.goto(x, y)

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()


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
        move_to_y = self.ycor() + 24
        self.shape("..\\Images\\70\\UP.gif")
        self.goto(move_to_x, move_to_y)

    def go_down(self):
        print("Player go down")
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        self.shape("..\\Images\\70\\DOWN.gif")
        if (move_to_x, move_to_y) not in walls:
            self.position.x += 1
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        print("Player go left")
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        self.shape("..\\Images\\70\\LEFT.gif")
        self.goto(move_to_x, move_to_y)

    def go_right(self):
        print("Player go right")
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        self.shape("..\\Images\\70\\RIGHT.gif")
        self.goto(move_to_x, move_to_y)

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

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance < 5:
            return True
        else:
            return False

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()





# Global variable
treats = []
ghosts = []
walls = ['']
walls_block = Wall()
player = Player()


# start position of character
def setup_maze(board, difficulty, init_index):
    player.position = init_index
    print("[Player's initial position]:",player.position.coordinate())
    # 288

    for i in range(len(board)):
        for j in range(len(board[i])):
            # get the character of each x,y coord
            unity = board[i][j]
            screen_x = ((-1) * val_x) + (j * 24)
            screen_y = val_y - (i * 24)
            # printing the maze
            if unity == WALL:
                walls_block.goto(screen_x, screen_y)
                # walls_block.shape('Wall.gif')
                walls_block.stamp()
                # Add co-ordinates to list
                walls.append((screen_x, screen_y))
            elif unity == TREAT:
                treats.append(Treasure(screen_x, screen_y))
            elif unity == MONSTER and difficulty != 1:
                num = len(ghosts)
                ghosts.append(Ghost(screen_x, screen_y, num))
    # print Player according to its given location
    player.goto(((-1) * val_x) + (player.position.y * 24), val_y - (player.position.x * 24))
    # :)
    window.update()


def score_evaluation(gold, died, total_time):
    dc = DEATH_COST if died else 0
    return gold - dc - total_time * TCPS


def show_score(step, died, treats_left):
    score = score_evaluation(player.gold, died, step)
    mesg = "You WON" if not treats_left else "You DIED"
    mesg += ", Score = {}, took {} step".format(score, step)
    print("[RESULT]:" + mesg)
    messagebox.showinfo("Congratulations!!!!", mesg)


def endGame():
    print("[Game closed]")
    sys.exit()


def startGame(data: Map):
    step = 1
    start_time = time.time()
    setup_maze(data.maze_data, difficulty, data.pacman_init_position)

    treats_left = bool(maze.treats)
    died = False
    explored = [player.position.coordinate()]
    path = [player.position.coordinate()]
    ghost = difficulty > 1
    dead_path = []

    ghost_appearance = []
    dict_for_ghost_tracing = {}

    while treats_left or not died:
        # Time delay
        time.sleep(DELAY_TIME)
        #input("HAHA")
        # Check collision
        for ghost in ghosts:
            if player.is_collision(ghost):
                player.gold -= DEATH_COST
                print("Player died!!")
                player.destroy()
                died = True

        # Check alive
        print("------------------------Step level: ", step)
        print("Position:", player.position.coordinate())
        if not died:
            print("current position:", player.position.coordinate())
            # Think next move base on dificulty


            location = player.position.coordinate()
            # leave trail for ghosts to follow
            dict_for_ghost_tracing[location] = step
            next_move = Level4.level4(data, player.position, path, dead_path)



            print("------------------------end")
            cur_pos = player.position.coordinate()
            if next_move == "Stuck":
                print("Stuck")
                dead_path.append(cur_pos)
                # remove current and node before to go back
                path.clear()
                # del path[-2:-1]
            else:
                player.move(next_move)
                path.append(player.position.coordinate())
                explored.append(player.position.coordinate())

            for treat in treats:
                if player.is_collision(treat):
                    # Add the treat gold to the player gold
                    player.gold += treat.gold
                    print('Player Gold: {}'.format(player.gold))
                    data.maze_data[player.position.x][player.position.y] = 0
                    data.treats.remove(player.position)

                    #if not maze.treats:
                    if not data.treats:
                        treats_left = False
                    # Destroy the treat
                    treat.destroy()
                    # Remove the treat
                    treats.remove(treat)
            # double check
            for ghost in ghosts:
                if player.is_collision(ghost):
                    player.gold -= 1000
                    print("Player died!!")
                    player.destroy()
                    died = True


        # Update screen

        window.update()
        if not treats_left or died:
            print("END game")
            end_time = time.time()
            total_time = int(end_time - start_time)
            show_score(step, died, treats_left)
            endGame()
        step += 1

    # turtle.exitonclick()
    endGame()


if __name__ == "__main__":
    input_list = InputHandle()
    input_list.items()
    map = input_list.get_map("Maze2.txt")
    #maze = input_list.get_maze("Stuckin.txt")`
    # maze.print_raw_data()
    # maze.print_entities()
    #messagebox.showinfo("UI will started!!","Click ok to start!!!")
    startGame(mape)


