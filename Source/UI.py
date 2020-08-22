import turtle
from tkinter import messagebox
import time
# offset stuff
val_x = 400
val_y = 350
# --------------------------------------------Initial things-----------------------------
window = turtle.Screen()
root = turtle.Screen()._root
window.bgcolor('black')
window.title('AI WUMPUS')
window.setup([1000,800], startx=0, starty=20)
window.tracer(0)
# --------------------------------------------------
images = ["..\\Images\\70\\DOWN.gif",
          "..\\Images\\70\\LEFT.gif",
          "..\\Images\\70\\RIGHT.gif",
          "..\\Images\\70\\UP.gif",
          "..\\Images\\70\\WUMPUS.gif"]
for img in images:
    turtle.register_shape(img)


class Unknown(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('blue')
        self.penup()
        self.speed(0)

class Known(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('purple')
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self, init_pos: Point = None):
        turtle.Turtle.__init__(self)
        self.position = init_pos if init_pos else Point()
        self.shape("..\\images\\gif\\pacman_right.gif")
        self.color('gold')
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        print("Pacman go up")
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        self.shape("..\\images\\gif\\pacman_up.gif")
        if (move_to_x, move_to_y) not in walls:
            self.position.x -= 1
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        print("Pacman go down")
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        self.shape("..\\images\\gif\\pacman_down.gif")
        if (move_to_x, move_to_y) not in walls:
            self.position.x += 1
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        print("Pacman go left")
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        self.shape("..\\images\\gif\\pacman_left.gif")
        if (move_to_x, move_to_y) not in walls:
            self.position.y -= 1
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        print("Pacman go right")
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        self.shape("..\\images\\gif\\pacman_right.gif")
        if (move_to_x, move_to_y) not in walls:
            self.position.y += 1
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


class Ghost(turtle.Turtle):
    def __init__(self, x, y, num):
        turtle.Turtle.__init__(self)
        self.num = num

        if self.num == 0:
            self.shape("..\\images\\gif\\Blue_left.gif")
        elif self.num == 1:
            self.shape("..\\images\\gif\\Orange_left.gif")
        elif self.num == 2:
            self.shape("..\\images\\gif\\Pink_left.gif")
        elif self.num == 3:
            self.shape("..\\images\\gif\\Red_left.gif")
        else:
            self.shape("..\\images\\gif\\White_left.gif")

        self.color("green")
        self.penup()
        self.speed(0)
        # self.gold = 25
        self.goto(x, y)
        # self.direction = random.choice(["up", "down", "right", "left"])
        self.direction_to_init = None
        self.rotate = 0
        self.previous_move = None
    def coord(self):
        return (self.xcor(), self.ycor())

    def destroy(self):
        self.goto(2000, 2000)
        self.hideturtle()

    def go_forward(self, direction):
        move_to_x = self.xcor()
        move_to_y = self.ycor()
        if direction == "Up":
            move_to_y += 24
        elif direction == "Down":
            move_to_y -= 24
        elif direction == "Right":
            move_to_x += 24
            if self.num == 0:
                self.shape("..\\images\\gif\\Blue_right.gif")
            elif self.num == 1:
                self.shape("..\\images\\gif\\Orange_right.gif")
            elif self.num == 2:
                self.shape("..\\images\\gif\\Pink_right.gif")
            elif self.num == 3:
                self.shape("..\\images\\gif\\Red_right.gif")
            else:
                self.shape("..\\images\\gif\\White_right.gif")
        elif direction == "Left":
            move_to_x -= 24
            if self.num == 0:
                self.shape("..\\images\\gif\\Blue_left.gif")
            elif self.num == 1:
                self.shape("..\\images\\gif\\Orange_left.gif")
            elif self.num == 2:
                self.shape("..\\images\\gif\\Pink_left.gif")
            elif self.num == 3:
                self.shape("..\\images\\gif\\Red_left.gif")
            else:
                self.shape("..\\images\\gif\\White_left.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.forward(0)
            return True
        return False

    def go_backward(self, direction):
        move_to_x = self.xcor()
        move_to_y = self.ycor()
        if direction == "Down":
            move_to_y += 24
        elif direction == "Up":
            move_to_y -= 24
        elif direction == "Left":
            move_to_x += 24
            if self.num == 0:
                self.shape("..\\images\\gif\\Blue_right.gif")
            elif self.num == 1:
                self.shape("..\\images\\gif\\Orange_right.gif")
            elif self.num == 2:
                self.shape("..\\images\\gif\\Pink_right.gif")
            elif self.num == 3:
                self.shape("..\\images\\gif\\Red_right.gif")
            else:
                self.shape("..\\images\\gif\\White_right.gif")
        elif direction == "Right":
            move_to_x -= 24
            if self.num == 0:
                self.shape("..\\images\\gif\\Blue_left.gif")
            elif self.num == 1:
                self.shape("..\\images\\gif\\Orange_left.gif")
            elif self.num == 2:
                self.shape("..\\images\\gif\\Pink_left.gif")
            elif self.num == 3:
                self.shape("..\\images\\gif\\Red_left.gif")
            else:
                self.shape("..\\images\\gif\\White_left.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.forward(0)
            return True
        return False

    def move(self):
        if self.direction_to_init == None:
            # clock-wise move-ment
            directions_list = ["Up", "Right", "Down", "Left"]
            count = 0
            i = self.rotate
            if i == 3:
                i = 0
            elif i >= 0 and i < 3:
                i += 1
            while count < 4:
                count += 1
                try_val = self.go_forward(directions_list[i])
                if try_val:
                    self.direction_to_init = directions_list[i]
                    break
                else:
                    if i == 3:
                        i = 0
                    elif i >= 0 and i < 3:
                        i += 1
            self.forward(0)
            self.rotate = i
        else:
            try_val = self.go_backward(self.direction_to_init)
            self.forward(0)
            if not try_val:
                print("[Error]: Something went wrong in ghost's movement to get back to initial place")
            self.direction_to_init = None



class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("..\\images\\gif\\fruit.gif")
        self.color('black')
        self.penup()
        self.speed(0)
        self.gold = GOLD
        self.goto(x, y)

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


def startGame(data: Maze, difficulty):
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
            if difficulty < 3:
                # next_move = Level1.level1(maze, player.position, path, dead_path, ghost)
                next_move = Level1.level1(data, player.position, path, dead_path, ghost)
                # Move
                #print("Dead path: ", dead_path)
                #print("Explored: ", explored)

            elif difficulty == 3:
                next_move = Level3.level3(data, player.position, path, dead_path, ghost_appearance)
                # in case pac man get stuck between a corner and a ghost
                if next_move == "Stuck" and ghost_appearance:
                    ghost_appearance.pop()
                print("--------------ghosts location:\n", [i.coordinate() for i in ghost_appearance])
            elif difficulty == 4:
                location = player.position.coordinate()
                # leave trail for ghosts to follow
                dict_for_ghost_tracing[location] = step
                next_move = Level4.level4(data, player.position, path, dead_path)
            else:
                next_move = "Nah???"

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
                if difficulty > 2:
                    """
                    # How turtle tiles's location was set from maze coordinate
                    screen_x = ((-1) * val_x) + (j * 24)
                    screen_y = val_y - (i * 24)
                    """
                    previous_pos = ghost.coord()
                    pos_x = int((val_y - previous_pos[1]) / 24)
                    pos_y = int((previous_pos[0] + val_x) / 24)
                    data.maze_data[pos_x][pos_y] = 0
                    #print("Ghost move from:", pos_x, pos_y)
                    if difficulty == 3:
                        ghost.move()
                    elif difficulty == 4:
                        ghost_point = Point(pos_x, pos_y)
                        g_move = Level4.ghost_move(data, ghost_point, dict_for_ghost_tracing, player.position, step, ghost.previous_move)
                        ghost.previous_move = g_move
                        if g_move == "Stuck":
                            ghost.move()
                            ghost.forward(0)
                        else:
                            valid_move = ghost.go_forward(g_move)
                            ghost.forward(0)
                            if not valid_move:
                                print("---------------------Ghost hit walls - WTF! this is not suppose to happen")
                    new_pos = ghost.coord()
                    #print("here")
                    pos_x = int((val_y - new_pos[1]) / 24)
                    pos_y = int((new_pos[0] + val_x) / 24)
                    data.maze_data[pos_x][pos_y] = 3
                    #print("to:", pos_x, pos_y)

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
    maze = input_list.get_maze("Maze2.txt")
    #maze = input_list.get_maze("Stuckin.txt")`
    # maze.print_raw_data()
    # maze.print_entities()
    difficulty = 4
    #messagebox.showinfo("UI will started!!","Click ok to start!!!")
    startGame(maze, difficulty)


