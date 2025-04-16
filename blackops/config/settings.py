# -----------------------------
# config/settings.py
# -----------------------------
import os
import yaml

def load_config():
    file_path = os.path.join(os.getcwd(), 'config', 'settings.yaml')

    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)

    return config