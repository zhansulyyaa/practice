import json, os

DEFAULT = {
    "snake_color": [0, 200, 0],
    "grid":        False,
    "sound":       True
}

def load():
    if not os.path.exists("settings.json"):
        save(DEFAULT.copy())
        return DEFAULT.copy()
    with open("settings.json") as f:
        return json.load(f)

def save(s):
    with open("settings.json", "w") as f:
        json.dump(s, f, indent=2)
