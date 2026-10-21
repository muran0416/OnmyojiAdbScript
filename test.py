import time, subprocess

ADB="adb"
DEVICE_ID="127.0.0.1:16416"

subprocess.run(f"{ADB} connect {DEVICE_ID}", shell=True)

# 点屏幕正中间
# subprocess.run(f"{ADB} -s {DEVICE_ID} shell input tap 640 360", shell=True)

# time.sleep(1)

# 再点一次
# subprocess.run(f"{ADB} -s {DEVICE_ID} shell input tap 640 360", shell=True)