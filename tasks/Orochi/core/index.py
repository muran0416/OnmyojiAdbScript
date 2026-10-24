import datetime
import time
import os
import json
import os
import json
import random
import subprocess
import cv2
import numpy as np

def now_timestamp():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    now_time = f'INFO           |{now_time}|'
    return now_time

def log_info(self) -> bool:
    print(f'{now_timestamp()}{self}')

def config(File="../config/config.json"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(BASE_DIR, File)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def tool(settings):
    result = subprocess.run(
        [settings['ADB'], "-s", settings['serial'], "exec-out", "screencap", "-p"],
        capture_output=True
    )
    img_bytes = result.stdout  # 这是 bytes（二进制）
    # 转成 numpy 数组
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    # 解码成图像
    screen = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return screen

def adb_tap(settings,x, y, z):
    RAND_OFFSET = z
    if RAND_OFFSET > 0:
        x += random.randint(-RAND_OFFSET, RAND_OFFSET)
        y += random.randint(-RAND_OFFSET, RAND_OFFSET)
    subprocess.run(f"{settings['ADB']} -s {settings['serial']} shell input tap {x} {y}", shell=True)
    return x,y


def is_button_enabled(screen, x, y, w, h):
    """判断按钮是否有足够的彩色像素。"""
    button = screen[y:y + h, x:x + w]
    if button.size == 0:
        return False

    # 去掉外侧一圈，减少周围背景的干扰
    margin_x = int(w * 0.15)
    margin_y = int(h * 0.15)
    button = button[
        margin_y:h - margin_y,
        margin_x:w - margin_x
    ]
    if button.size == 0:
        return False

    hsv = cv2.cvtColor(button, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    brightness = hsv[:, :, 2]

    # 饱和度较高，且不是过暗的像素，视为彩色像素
    colored = (saturation >= 60) & (brightness >= 60)
    colored_ratio = np.mean(colored)

    return colored_ratio >= 0.20

# if __name__ == "__main__":
#     screen = tool()
#     print(screen.shape)