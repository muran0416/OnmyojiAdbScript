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

def mian(settings,Frequency=50,Motion=False):
    cunten = {'name':None,'frequency':0,'counter':0}
    # screen = tool(settings) # 多余截图可删除(暂存...)
    # 在进入循环前加载所有模板，避免每轮识别都重复读取图片。
    # 获取 main.py 所在目录，使模板路径不受启动命令所在目录影响。
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for template in settings['templates']:
        # 将配置中的相对路径（如 templates/t1.png）拼接成完整路径。
        template_path = os.path.join(base_dir, template['file'])
        # 直接以灰度图读取模板，后续与灰度截图进行匹配。
        tpl_gray = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        # 图片不存在或无法解码时立即报错，避免后续匹配时才出错。
        if tpl_gray is None:
            raise FileNotFoundError(f'模板读取失败：{template_path}')
        # 将图像矩阵缓存到当前模板字典中，仅保存在内存，不写回 JSON。
        template['gray'] = tpl_gray

    while 1:
        for template in settings['templates']:

            screen = tool(settings)
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # 使用启动时缓存的模板；截图实时更新，模板不再重复读取。
            tpl_gray = template['gray']
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
                    if template.get("count_completion", False):
                        cunten["counter"] += 1
                        log_info(f'已运行{cunten["counter"]}次~')
                    cunten["frequency"] = 1
                cx, cy = adb_tap(settings,cx, cy, 3)
                log_info(
                    f'name={current_name}, '
                    f'frequency={cunten["frequency"]}, '
                    f'score={max_val:.4f}, '
                    f'center=({cx},{cy})'
                )
                # 开启后达到设定次数停止运行
                if Motion:
                    if cunten["counter"] >= Frequency:
                        log_info(f'已运行{cunten["counter"]}次,任务结束~ ')
                        return

        if cunten["frequency"] >= 3 :
            log_info(
                f'连续点击 {cunten["name"]} '
                f'{cunten["frequency"]} 次, 自动结束!'
            )
            break
        time.sleep(1)

if __name__ == "__main__":
    # 运行文件
    File = "../config/config02.json"
    settings  = config(File)
    log_info(settings ["config_name"])
    # 开启运行次数
    mian(settings,50,True)

    # 默认不开启
    # mian(settings)





