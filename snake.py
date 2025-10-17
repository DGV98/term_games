import curses
from random import randint


class Node:
    """
    This is the utility class for a Linked List, will be used to create a snake
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.next = None


class Snake:
    """
    Snake class, essentially a pointer to the head and tail of the linked list
    """

    def __init__(self, head: Node):
        self.head = head
        self.tail = head
        self.length = 1

    def grow(self, node: Node):
        """
        Attaches a node to the end of the linked list and updates the length

        Args:
            node (Node): The node to add to the linked list
        """
        self.tail.next = node
        self.tail = self.tail.next
        self.length += 1


class GridState:
    """
    Class to keep track of the grid state, the snake, and updating everything regarding the game.
    """

    def __init__(self, max_y: int, max_x: int):
        self.width = max_x - 2
        self.height = max_y - 1
        head_x, head_y = self.width // 2, self.height // 2
        self.grid = [[" "] * self.width for i in range(self.height)]
        head = Node(head_x, head_y)
        self.head = "^"
        self.snake = Snake(head)
        self.food_x = 0
        self.food_y = 0
        self.generate_food()
        self.update_grid()
        self.exit_flag = False

    def game_cases(self, key):
        """
        The game cases, either collision or growth

        Args:
            key (string): the direction to move the head of the snake
        """
        self.update_snake_head(key)
        if self.snake.head.x == self.width or self.snake.head.x < 0:
            self.exit_flag = True
            return
        elif self.snake.head.y == self.height or self.snake.head.y < 0:
            self.exit_flag = True
            return
        elif self.grid[self.snake.head.y][self.snake.head.x] == "#":
            self.exit_flag = True
            return
        elif self.snake.head.x == self.food_x and self.snake.head.y == self.food_y:
            new_node = Node(self.snake.tail.x, self.snake.tail.y)
            self.snake.grow(new_node)
            self.generate_food()
        self.update_grid()

    def update_grid(self):
        """
        Updates the grid with the relevant information stored in the linked list and food object
        """
        self.grid[self.food_y][self.food_x] = "@"
        curr = self.snake.head.next
        while curr:
            self.grid[curr.y][curr.x] = "#"
            curr = curr.next
        self.grid[self.snake.head.y][self.snake.head.x] = self.head

    def update_snake_head(self, key):
        """
        Updates the head of the snake based on the direction, and updates the rest of the snake using update_snake

        Args:
            key (str): The direction from the key presses
        """
        prev_x, prev_y = self.snake.head.x, self.snake.head.y
        if key == curses.KEY_UP:  # Up arrow
            self.snake.head.y -= 1
            self.head = "^"
        elif key == curses.KEY_DOWN:  # Down arrow
            self.snake.head.y += 1
            self.head = "v"
        elif key == curses.KEY_RIGHT:  # Right arrow
            self.snake.head.x += 1
            self.head = ">"
        elif key == curses.KEY_LEFT:  # Left arrow
            self.snake.head.x -= 1
            self.head = "<"
        self.update_snake(prev_x, prev_y, self.snake.head.next)

    def update_snake(self, prev_x, prev_y, node: Node):
        """
        Recursive function to update the other nodes of the snake based on the direction of the head

        Args:
            prev_x (int): previous x position
            prev_y (int): previous y position
            node (Node): the node to update
        """
        if not node:
            self.grid[prev_y][prev_x] = " "
            return
        tmp_x, tmp_y = node.x, node.y
        node.x, node.y = prev_x, prev_y
        self.update_snake(tmp_x, tmp_y, node.next)

    def generate_food(self):
        """
        Update the food position in the grid
        """
        x = randint(0, self.width - 1)
        y = randint(0, self.height - 1)
        while self.grid[y][x] == "#" or (x, y) == (
            self.snake.head.x,
            self.snake.head.y,
        ):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
        self.food_x = x
        self.food_y = y


def paint_screen(win: curses.window, grid: GridState):
    win.box()
    for i, line in enumerate(grid.grid):
        win.addstr(i + 1, 1, "".join(line))
    win.refresh()


def play_snake(stdscr: curses.window, win1: curses.window, win2: curses.window):
    """
    Play the game, main game loop, will be threaded along with the key strokes
    """
    max_y, max_x = win2.getmaxyx()
    grid = GridState(max_y - 1, max_x)
    paint_screen(win2, grid)
    while True:
        score = f"SCORE: {grid.snake.length}"
        x = (max_x - len(score)) // 2
        win1.addstr(6, x, score)
        win1.refresh()
        key = stdscr.getch()
        if key == ord("q"):
            return grid.snake.length
        else:
            if key in [
                curses.KEY_UP,
                curses.KEY_DOWN,
                curses.KEY_RIGHT,
                curses.KEY_LEFT,
            ]:
                grid.game_cases(key)
                if grid.exit_flag:
                    return grid.snake.length
            paint_screen(win2, grid)
