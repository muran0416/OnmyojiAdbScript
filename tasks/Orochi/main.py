import os
import json
import random
import subprocess
import time

import cv2
import numpy as np
from core.index import log_info
from core.index import config
from core.index import tool
from core.index import adb_tap

def mian():
    cunten = {'name':None,'frequency':0,'counter':0}
    while 1:
        for template in config['templates']:

            screen = tool()
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            tpl_gray = cv2.cvtColor(cv2.imread(template['file']), cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(screen_gray, tpl_gray, cv2.TM_CCOEFF_NORMED)

            # max_val 匹配值，越大匹配越精确
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            h, w = tpl_gray.shape[:2]
            x0, y0 = max_loc
            cx, cy = x0 + w // 2, y0 + h // 2
            if max_val > 0.90:
                current_name = template["name"]
                if cunten["name"] == current_name:
                    # 和上次匹配相同
                    cunten["frequency"] += 1
                else:
                    # 和上次匹配不同
                    cunten["name"] = current_name
                    cunten["counter"] += 1
                    cunten["frequency"] = 1
                cx, cy = adb_tap(cx, cy, 3)
                log_info(
                    f'name={current_name}, '
                    f'frequency={cunten["frequency"]}, '
                    f'score={max_val:.4f}, '
                    f'center=({cx},{cy})'
                )
        if cunten["frequency"] >= 3 :
            log_info(
                f'连续点击 {cunten["name"]} '
                f'{cunten["frequency"]} 次, 自动结束!'
            )
            break
        if cunten["counter"]/len(config["templates"]) >= 50:
            log_info(f'已运行{cunten["counter"]/len(config["templates"])}次,任务结束~ ')
            break

        time.sleep(2)

if __name__ == "__main__":
    config = config()
    log_info(config["config_name"])
    mian()





