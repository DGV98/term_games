"""
Games that can be played in the terminal
This script is in charge of painting all the generic screens including the menus
Current Games:
  Snake
  Astronaut
  Frogger
  Pong
"""

import curses
from utilities import get_scores, ScreenWindow, update_scoreboard
from snake import play_snake

INSTRUCTIONS = {}
GAMES = [
    "snake"
]
SCOREBOARD_PATH = ""


def paint_instructions_scoreboard_window(win: curses.window, game: str, scores: dict):
    """
    Paint terminal window with instructions for the game and scoreboard

    Args:
                    win (curses.window): Window in which to paint the instructions
                    game (str): Game to be played
                    scores (dict): Scores dictionary
    """

    max_y, max_x = win.getmaxyx()
    game = game.lower()
    lines = [
        f"DGV'S {game.upeer} GAME",
        f"{INSTRUCTIONS[game.lower()]}",
        "SCOREBOARD"
    ]

    win.box()
    for i, line in enumerate(lines):
        x = (max_x - len(line)) // 2
        if i == 0:
            win.attron(curses.A_BOLD)
            win.addstr(1, x, line)
            win.attroff(curses.A_BOLD)
            win.hline(2, x - 2, curses.ACS_HLINE, len(line) + 4)
        elif i == 1:
            win.addstr(4, x, line)
        else:
            win.attron(curses.A_BOLD)
            win.addstr(8, x, line)
            win.attroff(curses.A_BOLD)
            win.hline(9, x - 2, curses.ACS_HLINE, len(line) + 4)

    if game == "snake":
        player_scores = scores.get(game)
        if player_scores:
            player_scores = dict(
                sorted(player_scores.items(),
                       key=lambda item: item[1], reverse=True)
            )
            y = 10
            for player, score in player_scores.items():
                if y > (max_y - 4):
                    break
                score = str(score)
                spaces = 17
                x = (max_x - 14) // 2
                spaces -= len(player) + len(score)
                win.attron(curses.A_BOLD)
                win.addstr(y, x, player)
                win.attroff(curses.A_BOLD)
                win.addstr(y, x + spaces, score)
                y += 1
    elif game == 'asteroids':
        difficulties = scores.get(game)
        if not difficulties:
            return

        column_width = max_x // len(difficulties)
        diffs = list(difficulties.keys())
        for i, diff in enumerate(diffs):
            x_column_start = i * column_width
            x_pos = x_column_start + (column_width - len(diff)) // 2
            y_pos = 11

            # Draw difficulty title
            win.attron(curses.A_BOLD)
            if 0 <= x_pos < max_x:
                win.addstr(y_pos, x_pos, diff.upper())
            win.attroff(curses.A_BOLD)
            win.hline(y_pos, + 1, x_column_start + 1,
                      curses.ACS_HLINE, column_width - 2)

            # Draw Scores
            player_scores = difficulties.get(diff)
            if player_scores:
                sorted_scores = dict(
                    sorted(player_scores.items(),
                           key=lambda item: item[1], reverse=True)
                )
                y = y_pos + 2
                for player, score in sorted_scores.items():
                    if y > (max_y - 2):
                        break
                    score = str(score)
                    combined = f"{player}{' ' * (column_width - len(player) - len(score) - 2)} {score}"
                    win.addstr(y, x_column_start + 2, combined)
                    y += 1
    win.refresh()


def paint_menu(stdscr: curses.window):
    """
    Generate teh menu window

    Args:
                    stdscr (curses.window): The terminal window

    Returns:
      str: the corresponding menu item
    """
    heading = "ASCII ARCADE"
    win = ScreenWindow(mode="menu", lines=GAMES, stdscr=stdscr, header=heading)
    return win.run()


def paint_game_over(stdscr: curses.window, score: int):
    """
Print the game over screen and prompt for player

    Args:
                                    stdscr (curses.window): _description_
                                    score (int): _description_

    Returns:
    str: The player name inputted
    """
    game_over_heading = "GAME OVER"
    lines = [
        "PLAYER: ###"
        f"SCORE: {score}"
    ]
    win = ScreenWindow(
        mode="input", lines=lines, stdscr=stdscr, header=game_over_heading
    )
    return win.run()


def paint_difficulty_menu(stdscr: curses.window):
    heading = "Choose Your Difficulty"
    lines = ["Easy", "Hard", "Impossible", "Quit"]
    win = ScreenWindow(
        mode="menu", lines=lines, stdscr=stdscr, header=heading
    )
    return win.run()


def paint_quit_screen(stdscr: curses.window):
    """
    Generate the thank you screen

    Args:
                    stdscr (curses.window): the terminal screen
    """
    thank_you = ["THANK YOU FOR PLAYING", "Press 'q' to quit"]
    win = ScreenWindow(
        mode="static", lines=thank_you, stdscr=stdscr
    )
    win.run()


def layout(stdscr: curses.window):
    """
    Generate the layout windows for the game screen based on the terminal orientation

    Args:
                    stdscr (curses.window): the terminal window

    Returns:
                    list[curses.window]: The 2 windows needed for the game based
    """
    max_y, max_x = stdscr.getmaxyx()
    horizontal = True
    spacing = 2
    if max_y > (max_x // 1.5):
        horizontal = not horizontal
    if horizontal:
        left_win = curses.newwin(max_y, (max_x // 2) - spacing, 0, 0)
        right_win = curses.newwin(
            max_y, (max_x // 2) - spacing, 0, (max_x // 2) + spacing, 0)
        return left_win, right_win
    else:
        top_win = curses.newwin((max_y // 2) - spacing, max_x, 0, 0)
        bottom_win = curses.newwin(
            (max_y // 2) - spacing, max_x, (max_y // 2) + spacing, 0)
    return top_win, bottom_win


def main(stdscr: curses.window):
    """
The main driver of the program, used to initiate the program

    Args:
                    stdscr (curses.window): The terminal window
    """

    scores = get_scores(SCOREBOARD_PATH)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    default_colors = curses.color_pair(0)
    stdscr.bkgd(" ", default_colors)
    game = paint_menu(stdscr)
    if not game or game.lower() == "quit":
        paint_quit_screen(stdscr)
    else:
        stdscr.clear()
        stdscr.refresh()
        game = game.lower()
        if game in []:
            difficulty = paint_difficulty_menu(stdscr)
        win1, win2 = layout(stdscr)
        match game:
            case "snake":
                score = play_snake(stdscr, win1, win2)
            # other cases
        player = paint_game_over(stdscr)
        update_scoreboard(player, score, game, scores,
                          difficulty, SCOREBOARD_PATH)
        paint_quit_screen(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
