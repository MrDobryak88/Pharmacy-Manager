import json
import os
import sys

class Config:
    def __init__(self):
        # Use dynamic path for config.json
        if getattr(sys, 'frozen', False):
            # Running as EXE
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as script
            base_path = os.path.abspath(os.path.dirname(__file__))
        self.config_file = os.path.join(base_path, "config.json")
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "theme": "light",
                "bg_color": "#2b2d30",
                "font_size": "14px",
                "button_style": "С тенями",
                "language": "Русский"
            }
            self.save_config()

    def save_config(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()