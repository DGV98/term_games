# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
python games.py
```

No external dependencies - uses only Python standard library (curses, json, random).

## Architecture

Terminal-based game framework using Python curses with a two-window layout system.

### Core Components

- **games.py** - Main entry point and menu orchestration. Contains `main()` which initializes curses, displays menus, routes to games, and handles the game-over flow. The `layout()` function creates a responsive two-window setup (left: info/scores, right: game board) that adapts based on terminal orientation.

- **utilities.py** - Reusable UI system built around `ScreenWindow` class which supports three modes:
  - `"menu"` - Selectable list with vim-style (j/k) or arrow key navigation
  - `"input"` - Text input with validation (4-30 chars)
  - `"static"` - Read-only display screens

  Also contains `get_scores()` and `update_scoreboard()` for JSON-based score persistence.

- **snake.py** - Snake game implementation using a linked list data structure (`Node`, `Snake` classes) for efficient body management. `GridState` handles all game logic including movement, collision detection, and food generation.

### Game Flow

1. `main()` loads scores from `scoreboard.json`
2. `paint_menu()` shows game selection via `ScreenWindow`
3. `layout()` creates two curses windows based on terminal size
4. Game function (e.g., `play_snake()`) runs with both windows
5. `paint_game_over()` prompts for player name
6. `update_scoreboard()` saves high score
7. `paint_quit_screen()` shows exit message

### Adding New Games

1. Create game file with a `play_<game>(stdscr, win1, win2) -> int` function
2. Add game name to `GAMES` list in games.py
3. Add case to match statement in `main()`
4. Add instructions to `INSTRUCTIONS` dict
