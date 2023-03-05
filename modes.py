import os
import json

run_settings_location = "run_data/run_settings.json"
if os.path.exists(run_settings_location):
    with open(run_settings_location, 'r') as file:
        file_contents = json.load(file)

JARVIS = file_contents["chat_system_settings"]

THREE_WORDS = "You can only answer using 3 words."

TEST = 'O'