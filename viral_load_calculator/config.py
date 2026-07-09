# config.py
import json
import os
import sys
from pathlib import Path


def _get_user_config_dir():
    """Return a user-writable directory for settings.

    Uses platform-appropriate locations:
    - Linux: $XDG_CONFIG_HOME/viral-load-calculator (defaults to ~/.config/viral-load-calculator)
    - Windows: %APPDATA%/ViralLoadCalculator
    - macOS: ~/Library/Application Support/ViralLoadCalculator
    """
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.join(
            os.path.expanduser("~"), "AppData", "Roaming"
        )
        return os.path.join(base, "ViralLoadCalculator")
    if sys.platform == "darwin":
        return os.path.join(
            os.path.expanduser("~"), "Library", "Application Support",
            "ViralLoadCalculator",
        )
    xdg = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
        os.path.expanduser("~"), ".config"
    )
    return os.path.join(xdg, "viral-load-calculator")


def get_user_data_dir_or_file(file: str | None):
    if file is not None:
        return os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'), 'ViralLoadCalculator') + f'/{file}'
    return os.path.join(os.path.join(os.path.expanduser('~'), 'Desktop'), 'ViralLoadCalculator')


class Config:
    DEFAULTS = {
        "HBVL_CONSTANT": 0.167,
        "HCVL_CONSTANT": 0.57,
        "HIVL_CONSTANT": 0.57
    }

    @classmethod
    def _get_resource_path(cls, relative_path):
        """Get absolute path to bundled resource, works for dev and PyInstaller."""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = Path(__file__).resolve().parent.parent
        return os.path.join(base_path, relative_path)

    @classmethod
    def _get_user_config_file(cls):
        """Path to the user-writable settings file."""
        return os.path.join(_get_user_config_dir(), "settings.json")

    @classmethod
    def _get_config_file(cls):
        """Resolve the settings file path.

        Prefers the user-writable location. Falls back to the bundled
        resource path only as a last resort (read-only on installed apps).
        """
        user_path = cls._get_user_config_file()
        if os.path.exists(user_path):
            return user_path
        # First run: copy bundled defaults into the user location so writes
        # succeed and the user can later edit their own copy.
        bundled = cls._get_resource_path("resources/settings.json")
        try:
            os.makedirs(os.path.dirname(user_path), exist_ok=True)
            if os.path.exists(bundled):
                with open(bundled, "r") as src, open(user_path, "w") as dst:
                    dst.write(src.read())
            else:
                with open(user_path, "w") as f:
                    json.dump(cls.DEFAULTS, f, indent=4)
            return user_path
        except OSError:
            # Read-only filesystem (e.g. installed under /Program Files without
            # write perms). Fall back to the bundled read-only path.
            return bundled

    @classmethod
    def load(cls):
        """Load constants from the config file or return defaults."""
        try:
            with open(cls._get_config_file(), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return cls.DEFAULTS.copy()

    @classmethod
    def save(cls, data):
        """Save constants to the user-writable config file."""
        try:
            config_path = cls._get_user_config_file()
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(data, f, indent=4)
        except (PermissionError, OSError):
            # Read-only filesystem: silently skip. In-memory state in main.py
            # is unaffected; the next launch will reload from disk.
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