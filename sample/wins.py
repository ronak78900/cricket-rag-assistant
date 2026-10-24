import json


def load_matches(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)


def count_wins(matches: list[dict]) -> dict[str, int]:
    wins: dict[str, int] = {}
    for match in matches:
        winner = match["winner"]
        if winner is None:
            continue
        wins[winner] = wins.get(winner, 0) + 1
    return wins


if __name__ == "__main__":
    matches = load_matches("sample/matches.json")
    wins = count_wins(matches)
    for team, count in sorted(wins.items(), key=lambda item: item[1], reverse=True):
        print(f"{team}: {count}")