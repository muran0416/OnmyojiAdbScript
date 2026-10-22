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

def config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(BASE_DIR, "../config/config.json")

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

def tool():
    result = subprocess.run(
        [config()['ADB'], "-s", config()['serial'], "exec-out", "screencap", "-p"],
        capture_output=True
    )
    img_bytes = result.stdout  # 这是 bytes（二进制）
    # 转成 numpy 数组
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    # 解码成图像
    screen = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return screen

def adb_tap(x, y, z):
    RAND_OFFSET = z
    if RAND_OFFSET > 0:
        x += random.randint(-RAND_OFFSET, RAND_OFFSET)
        y += random.randint(-RAND_OFFSET, RAND_OFFSET)
    subprocess.run(f"{config()['ADB']} -s {config()['serial']} shell input tap {x} {y}", shell=True)
    return x,y

# if __name__ == "__main__":
#
#     screen = tool()
#     print(screen.shape)