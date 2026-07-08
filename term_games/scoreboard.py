import json
from pathlib import Path


def get_scoreboard_path() -> Path:
    """
    Get the path to the scoreboard file using XDG standard.
    Creates the directory if it doesn't exist.

    Returns:
        Path: Path to scoreboard.json
    """
    data_dir = Path.home() / ".local" / "share" / "tgames"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "scoreboard.json"


def get_scores() -> dict:
    """
    Load scores from the scoreboard file.

    Returns:
        dict: Scores dictionary, empty dict if file doesn't exist
    """
    scoreboard_path = get_scoreboard_path()
    if not scoreboard_path.exists():
        return {}
    with open(scoreboard_path, "r") as scoreboard:
        scores = json.load(scoreboard)
    return scores


def update_scoreboard(
    player: str,
    score: int,
    game: str,
    scores: dict,
    difficulty: str,
):
    """
    Update the json holding all the scores

    Args:
        player (str): The player
        score (int): The score
        game (str): The game being updated
        scores (dict): Current scores dictionary
        difficulty (str): Difficulty level (empty string if not applicable)
    """
    player = player.upper()
    game = game.lower()
    if difficulty:
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
                if player not in scores[game][difficulty]:
                    scores[game][difficulty][player] = score
                else:
                    scores[game][difficulty][player] = max(
                        score, scores[game][difficulty][player]
                    )

    scoreboard_path = get_scoreboard_path()
    with open(scoreboard_path, "w") as scoreboard:
        json.dump(scores, scoreboard)
