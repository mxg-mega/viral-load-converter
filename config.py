# config.py
import json
import os

class Config:
    CONFIG_FILE = "settings.json"
    DEFAULTS = {
        "HBVL_CONSTANT": 0.167,
        "HCVL_CONSTANT": 0.57,
        "HIVL_CONSTANT": 0.59
    }

    @classmethod
    def load(cls):
        """Load constants from the config file or create it with defaults."""
        if not os.path.exists(cls.CONFIG_FILE):
            cls.save(cls.DEFAULTS)
            return cls.DEFAULTS
        with open(cls.CONFIG_FILE, "r") as f:
            return json.load(f)

    @classmethod
    def save(cls, data):
        """Save constants to the config file."""
        with open(cls.CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def get_constant(cls, key):
        """Get a constant value by key."""
        returnValue =  cls.load().get(key, cls.DEFAULTS[key])
        print('{}'.format(returnValue))
        return returnValue

    @classmethod
    def set_constant(cls, key, value):
        """Update a constant and save to the config file."""
        data = cls.load()
        print("{}".format(data))
        data[key] = value
        print("{}: updated to '{}' ".format(key, value))
        cls.save(data)