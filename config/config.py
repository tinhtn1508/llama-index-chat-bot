import json

def load_config() -> dict:
    with open('config/config.json') as f:
        return json.load(f)

conf = load_config()