import os
import time
import random
import subprocess
import cv2


DEVICE_ID="127.0.0.1:16416"  # 你截图里就是这个
ADB = "adb"                    # 如果你想写绝对路径也行：r"E:\platform-tools\adb.exe"
SCREEN_PNG = "template.png"

# 通过ADB对屏幕进行截图，并保存在本地
def adb_screenshot():
    subprocess.run(
        f'{ADB} -s {DEVICE_ID} exec-out screencap -p > "{SCREEN_PNG}"',
        shell=True
    )
    return os.path.exists(SCREEN_PNG)
adb_screenshot()
