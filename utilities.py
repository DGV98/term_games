import curses
import json


class ScreenWindow:
    """
    The base window class for our use case
    """

    def __init__(
        self,
        stdscr: curses.window,
        mode: str,
        lines: list[str],
        header: str = "",
        input_line_idx: int = 0,
        padding: int = 2,
    ):
        self.stdscr = stdscr
        self.mode = mode
        self.header = header
        self.lines = lines
        self.input_line_idx = input_line_idx
        self.padding = padding
        self.selected_idx = 0  # for menu
        self.input_result = ""  # for input

        content_lines = [header] if header else []
        content_lines += lines
        self.width = max(len(line) for line in content_lines) + 2 * padding
        if self.mode == "input":
            self.width += 3
        self.height = len(lines) + 2 * padding + (2 if header else 0)

        max_y, max_x = stdscr.getmaxyx()
        y = (max_y - self.height) // 2
        x = (max_x - self.width) // 2
        self.win = curses.newwin(self.height, self.width, y, x)
        self.win.keypad(True)

    def get_win(self):
        """
        Window getting funtion to manipulate window object

        Returns:
            curses.window: the window object
        """
        return self.win

    def mv_win(self, y, x):
        self.win.mvwin(y, x)

    def draw(self):
        """
        Drawing all the content on the window
        """
        self.win.clear()
        self.win.box()
        y = self.padding

        if self.header:
            x = (self.width - len(self.header)) // 2
            self.win.addstr(y, x, self.header, curses.A_BOLD)
            y += 1
            self.win.hline(
                y, self.padding, curses.ACS_HLINE, self.width - 2 * self.padding
            )
            y += 1

        for idx, line in enumerate(self.lines):
            display = line
            attr = curses.A_NORMAL

            if self.mode == "menu" and idx == self.selected_idx:
                attr = curses.A_REVERSE

            x = (self.width - len(display)) // 2
            self.win.addstr(y + idx, x, display, attr)

        self.win.refresh()

    def run(self):
        """
        Runs the drawing function

        Returns:
            str or None: Depending on the type of screen, returns a string or nothing
        """
        self.stdscr.clear()
        self.stdscr.refresh()
        if self.mode == "static":
            self.draw()
            self.stdscr.getch()

        elif self.mode == "input":
            while True:
                self.draw()
                y = self.padding + (2 if self.header else 0) + self.input_line_idx
                x = self.padding + len(self.lines[self.input_line_idx]) - 2
                curses.echo()
                curses.curs_set(2)
                self.win.move(y, x)
                self.input_result = self.win.getstr(y, x, 30).decode("utf-8")
                curses.curs_set(0)
                curses.noecho()
                if len(self.input_result) < 4 and self.input_result:
                    break
            return self.input_result

        elif self.mode == "menu":
            while True:
                self.draw()
                key = self.stdscr.getch()

                if key in [curses.KEY_UP, ord("k")]:
                    self.selected_idx = (self.selected_idx - 1) % len(self.lines)
                elif key in [curses.KEY_DOWN, ord("j")]:
                    self.selected_idx = (self.selected_idx + 1) % len(self.lines)
                elif key in [curses.KEY_ENTER, 10, 13]:
                    return self.lines[self.selected_idx]


def get_scores(scoreboard_path):
    with open(scoreboard_path, "r") as scoreboard:
        scores = json.load(scoreboard)
    return scores


def update_scoreboard(
    player: str,
    score: int,
    game: str,
    scores: dict,
    difficulty: str,
    scoreboard_path: str,
):
    """
    Update the json holding all the scores

    Args:
        player (str): The player
        score (int): The score
        game (str): The game being updated
    """
    player = player.upper()
    game = game.lower()
    difficulty = difficulty.lower()
    if game not in scores:
        if not difficulty:
            scores[game] = {player: score}
        else:
            scores[game] = {difficulty: {player: score}}
    else:
        if not difficulty:
            if player not in scores[game]:
                scores[game][player] = score
            else:
                scores[game][player] = max(score, scores[game][player])
        else:
            if difficulty not in scores[game]:
                scores[game][difficulty] = {player: score}
            else:
                if player not in scores[game]:
                    scores[game][difficulty][player] = score
                else:
                    scores[game][difficulty][player] = max(score, scores[game][player])

    with open(scoreboard_path, "w") as scoreboard:
        json.dump(scores, scoreboard)
