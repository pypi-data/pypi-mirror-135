from typing import Dict, Any
from enum import Enum
from pathlib import Path
from clease import jsonio

__all__ = ["save_app_data", "load_app_data", "AppDataKeys"]


class AppDataKeys(str, Enum):
    """Collection of keys which (may) be in the app_data.
    Keys starting with an '_' will not be saved in the app state."""

    # "private" keys
    CWD = "_cwd"
    STATUS = "_status"
    DEV_MODE = "_dev_mode"

    # Regular app data keys
    SUPERCELL = "supercell"
    SETTINGS = "settings"
    ECI = "eci"
    CANONICAL_MC_DATA = "canonical_mc_data"

    # The evaluator cannot be saved to file, so save it as private
    # instance of an Evaluate class
    EVALUATE = "_evaluator"

    @classmethod
    def is_key_private(cls, key: str) -> bool:
        """Check if a given key is considered 'private'"""
        return key.startswith("_")

    @classmethod
    def is_key_public(cls, key: str) -> bool:
        """Check if a given key is considered 'public'"""
        return not cls.is_key_private(key)

    @classmethod
    def iter_public_keys(cls):
        yield from filter(cls.is_key_public, cls)

    @classmethod
    def iter_private_keys(cls):
        yield from filter(cls.is_key_private, cls)


def save_app_data(app_data: Dict[str, Any], fname):
    fname = Path(fname)
    data = app_data.copy()
    to_remove = []
    for key in data:
        # Find keys which we don't want to save
        # Any keys starting with a "_" we say
        # we don't want to save
        if AppDataKeys.is_key_private(key):
            to_remove.append(key)
    for key in to_remove:
        data.pop(key, None)

    with fname.open("w") as file:
        jsonio.write_json(file, data)


def load_app_data(fname):
    fname = Path(fname)
    with fname.open() as file:
        return jsonio.read_json(file)
