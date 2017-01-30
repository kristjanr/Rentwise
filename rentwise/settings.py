import importlib
import os

import re

"""
Loads settings file based on the value of the MODE environment variable.
"""

MODE = os.environ.get('MODE') or 'local'


def load_settings(env):
    module = importlib.import_module('rentwise.settings_' + env)
    settings = {k: v for k, v in module.__dict__.items()
                if not re.match('^(_|@)', k)}
    globals().update(settings)


# First load default settings and then override them with env specific settings
from .settings_default import *

load_settings(MODE)
