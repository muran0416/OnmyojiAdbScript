import cv2
import numpy as np
from typing import Dict, Optional, Tuple, List, Union
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TPL_DIR = os.path.join(BASE_DIR, "templates")
print(TPL_DIR)
TEMPLATES: List[dict] = [
    # name, filename, threshold, cooldown, click_delay, region(可选)
    {"name": "matching", "file": "matching.png", "threshold": 0.58, "cooldown": 2.0, "click_delay": 0.2},
    {"name": "check_exploration", "file": "check_exploration.png", "threshold": 0.60, "cooldown": 1.5, "click_delay": 0.2},

    # 例：只在某个区域找（更快）
    # {"name": "start_btn", "file": "start.png", "threshold": 0.70, "cooldown": 3.0, "click_delay": 0.1,
    #  "region": (800, 600, 400, 300)},
]