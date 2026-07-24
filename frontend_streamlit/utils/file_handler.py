import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_json(path):
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        return {}
    with open(full_path, "r") as f:
        return json.load(f)


def save_json(path, data):
    full_path = os.path.join(BASE_DIR, path)
    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)