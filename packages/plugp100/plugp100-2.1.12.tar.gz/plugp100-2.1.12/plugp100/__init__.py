# import actual context
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from .api import TapoDeviceState, TapoApiClient
from .discover import TapoApiDiscover
from .core.params import SwitchParams, LightParams

__all__ = [
    "TapoApiClient",
    "TapoDeviceState",
    "SwitchParams",
    "LightParams",
    "TapoApiDiscover"
]

from . import _version
__version__ = _version.get_versions()['version']
