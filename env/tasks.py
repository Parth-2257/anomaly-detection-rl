# Task definitions and management

import json
import os


def load_all_tasks(difficulty="easy"):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", f"{difficulty}.json")

    with open(file_path, "r") as f:
        data = json.load(f)

    return data
