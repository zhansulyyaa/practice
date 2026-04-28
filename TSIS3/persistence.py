import json, os

DEFAULT_SETTINGS = {
    "sound":      True,
    "car_color":  "red",
    "difficulty": "normal"
}

def load_settings():
    if not os.path.exists("settings.json"):
        return DEFAULT_SETTINGS.copy()
    with open("settings.json") as f:
        return json.load(f)

def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f, indent=2)

def load_leaderboard():
    if not os.path.exists("leaderboard.json"):
        return []
    with open("leaderboard.json") as f:
        return json.load(f)

def save_score(name, score, distance):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance})
    board.sort(key=lambda x: x["score"], reverse=True)
    with open("leaderboard.json", "w") as f:
        json.dump(board[:10], f, indent=2)
