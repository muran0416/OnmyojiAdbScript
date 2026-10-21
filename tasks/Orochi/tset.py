from paddleocr import PaddleOCR

# 初始化 OCR（中文）
ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 识别图片文件
result = ocr.ocr("templates/Leadership.png", cls=True)

# 输出识别结果
for line in result[0]:
    text = line[1][0]
    score = line[1][1]
    print(f"文字: {text}, 置信度: {score:.2f}")