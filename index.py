import os
import time
import random
import subprocess
import cv2
import numpy as np


# =========== 配置区 =============
DEVICE_ID = "127.0.0.1:16416"  # 你截图里就是这个
ADB = "adb"                    # 如果你想写绝对路径也行：r"E:\platform-tools\adb.exe"
SCREEN_PNG = "screen.png"
# 点击随机偏移（像素）
RAND_OFFSET = 3  # 0 关闭


"""
subprocess.run(...)：在 Python 里执行一条命令，就像你在 CMD/PowerShell 里敲一样
ADB = "adb"：表示调用系统里的 adb.exe（你已经配置好了 PATH 或绝对路径）
DEVICE_ID = "127.0.0.1:16384"：你模拟器的 adb 地址
这句相当于你手动敲：
adb connect 127.0.0.1:163
"""
# 通过ABD进行连接
def adb_connect():
    subprocess.run(f"{ADB} connect {DEVICE_ID}", shell=True)
adb_connect()


"""
这句命令等价于：
adb -s 127.0.0.1:16384 exec-out screencap -p：让设备把屏幕以 png 形式输出到“标准输出”
> "screen.png"：Windows 的重定向，把输出写入文件
所以最终得到本地文件：screen.png
最后 return os.path.exists(SCREEN_PNG)：检查文件存在不存在，作为“截图是否成功”的判断。
"""
# 通过ADB对屏幕进行截图，并保存在本地
def adb_screenshot():
    subprocess.run(
        f'{ADB} -s {DEVICE_ID} exec-out screencap -p > "{SCREEN_PNG}"',
        shell=True
    )
    return os.path.exists(SCREEN_PNG)
adb_screenshot()

"""
shell input tap x y：安卓里模拟一次触控点击
前面那段 RAND_OFFSET 是为了给点击点位加一点随机偏移（更像人手点）
等价于你手动敲：
adb -s 127.0.0.1:16384 shell input tap 640 693
"""
def adb_tap(x, y,z):
    RAND_OFFSET = z
    if RAND_OFFSET > 0:
        x += random.randint(-RAND_OFFSET, RAND_OFFSET)
        y += random.randint(-RAND_OFFSET, RAND_OFFSET)
    subprocess.run(f"{ADB} -s {DEVICE_ID} shell input tap {x} {y}", shell=True)

"""
screen.png 只是一个文件
imread() 会把文件变成“像素矩阵”
OpenCV 默认读取为 BGR 格式
"""
screen_bgr = cv2.imread(SCREEN_PNG)
print(screen_bgr.shape)
print(screen_bgr[100, 200])

# 把三通道变成单通道
screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
print(screen_gray.shape)


# res = cv2.matchTemplate(screen_gray, tpl_gray, cv2.TM_CCOEFF_NORMED)