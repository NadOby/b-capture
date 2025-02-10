import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Loads configuration from file or returns defaults."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {"video_save_path": "videos/", "youtube_api_key": ""}

def save_config(config):
    """Saves configuration to file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
