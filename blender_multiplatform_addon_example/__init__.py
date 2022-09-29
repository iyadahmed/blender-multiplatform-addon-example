from pathlib import Path

from .platform_utils import setup_site_packages  # type: ignore

bl_info = {
    "name": "Multi-Platform Add-on Example",
    "author": "Iyad Ahmed",
    "version": (0, 0, 1),
    "blender": (3, 3, 0),
    "location": "",
    "description": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Example",
}


setup_site_packages(Path(__file__).parent / "lib")

import scipy
import numpy as np


def register():
    print(scipy.__version__)
    print(np.version.version)


def unregister():
    pass
