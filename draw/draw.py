import cv2

screen = cv2.imread("template.png")
tpl = cv2.imread("img.png")

screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)

res = cv2.matchTemplate(screen_gray, tpl_gray, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(res)

h, w = tpl_gray.shape[:2]
x0, y0 = max_loc
cx, cy = x0 + w // 2, y0 + h // 2

print("template (w,h):", (w, h))
print("score:", max_val)
print("top-left:", (x0, y0))
print("center:", (cx, cy))

# 画出来验证
cv2.rectangle(screen, (x0, y0), (x0 + w, y0 + h), (0, 255, 0), 2)
cv2.circle(screen, (cx, cy), 6, (0, 0, 255), -1)
cv2.imwrite("debug_box.png", screen)
print("saved debug_box.png")