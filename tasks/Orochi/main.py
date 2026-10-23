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
from core.index import is_button_enabled

def mian(Frequency=50):
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
                # 判断是否需要进行颜色判断,默认False
                if template.get("check_color", False):
                    if not is_button_enabled(screen, x0, y0, w, h):
                        # 组队界面挑战按钮为灰色,则跳过当前循环,不执行点击
                        continue
                if cunten["name"] == current_name:
                    # 和上次匹配相同
                    cunten["frequency"] += 1
                else:
                    # 和上次匹配不同
                    cunten["name"] = current_name
                    cunten["counter"] += 1
                    len(f'已运行{cunten["counter"]/len(config["templates"])}次~')
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
        if cunten["counter"]/len(config["templates"]) >= Frequency:
            log_info(f'已运行{cunten["counter"]/len(config["templates"])}次,任务结束~ ')
            break

        time.sleep(2)

if __name__ == "__main__":
    # 运行文件
    File = "../config/config.json"
    # 运行次数
    Runs = 50
    config = config(File)
    log_info(config["config_name"])
    mian(Runs)





