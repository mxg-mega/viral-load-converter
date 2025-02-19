# config.py
import json
import os
import sys

class Config:
    DEFAULTS = {
        "HBVL_CONSTANT": 0.167,
        "HCVL_CONSTANT": 0.57,
        "HIVL_CONSTANT": 0.59
    }

    @classmethod
    def _get_resource_path(cls, relative_path):
        """Get absolute path to resource, works for dev and PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @classmethod
    def _get_config_file(cls):
        """Get the config file path"""
        return cls._get_resource_path("resources/settings.json")

    @classmethod
    def load(cls):
        """Load constants from the config file or create it with defaults."""
        try:
            with open(cls._get_config_file(), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # For bundled app, we'll use defaults if file doesn't exist
            return cls.DEFAULTS.copy()

    @classmethod
    def save(cls, data):
        """Save constants to the config file."""
        try:
            config_path = cls._get_config_file()
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(data, f, indent=4)
        except PermissionError:
            # If we can't write to file (e.g., in program files), silently fail
            pass

    @classmethod
    def get_constant(cls, key):
        """Get a constant value by key."""
        return_value = cls.load().get(key, cls.DEFAULTS[key])
        print(f'{return_value}')
        return return_value

    @classmethod
    def set_constant(cls, key, value):
        """Update a constant and save to the config file."""
        data = cls.load()
        print(f"{data}")
        data[key] = value
        print(f"{key}: updated to '{value}'")
        cls.save(data)