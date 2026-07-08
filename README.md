# term_games

Terminal games you can play from your terminal. Layout is dynamic to orientation. Multiple games to choose from.

## Installation

```bash
pip install tgames
```

Or install from source:

```bash
git clone https://github.com/david/term_games.git
cd term_games
pip install -e .
```

## Usage

After installation, run:

```bash
tgames
```

Or run as a Python module:

```bash
python -m term_games
```

## Controls

- **Arrow keys** or **j/k**: Navigate menus
- **Enter**: Select
- **q**: Quit

## Games

- **Snake**: Classic snake game using arrow keys to move

## Scores

High scores are saved to `~/.local/share/tgames/scoreboard.json`

## Requirements

- Python >= 3.10
- No external dependencies (uses only Python standard library)

## TODOs

- Use sqlite database
- Start other games
- Put gameplay video in README
