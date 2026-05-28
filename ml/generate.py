# ml/generate.py
import cv2
import os
import random
import numpy as np
from PIL import Image, ImageDraw

# ── PATHS ──────────────────────────────────────────────
CLEANED_DIR  = "dataset/cleaned"
OUTPUT_PATH  = "public/generated/captcha.png"
IMG_SIZE     = 28
CAPTCHA_LEN  = 5

# ── PICK RANDOM DIGITS ─────────────────────────────────
answer = ""
char_images = []

for _ in range(CAPTCHA_LEN):
    digit = str(random.randint(0, 9))
    digit_folder = os.path.join(CLEANED_DIR, digit)
    img_file = random.choice(os.listdir(digit_folder))
    img_path = os.path.join(digit_folder, img_file)

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

    # ── RANDOM ROTATION ───────────────────────────────
    angle = random.randint(-25, 25)
    center = (IMG_SIZE // 2, IMG_SIZE // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(img, matrix, (IMG_SIZE, IMG_SIZE),
                         borderValue=0)

    char_images.append(img)
    answer += digit

# ── STITCH IMAGES SIDE BY SIDE ─────────────────────────
padding   = 10
cap_w     = IMG_SIZE * CAPTCHA_LEN + padding * (CAPTCHA_LEN + 1)
cap_h     = IMG_SIZE + padding * 2
canvas    = np.zeros((cap_h, cap_w), dtype=np.uint8)

for i, img in enumerate(char_images):
    x = padding + i * (IMG_SIZE + padding)
    y = padding
    canvas[y:y+IMG_SIZE, x:x+IMG_SIZE] = img

# ── ADD NOISE ──────────────────────────────────────────
noise = np.random.randint(0, 60, canvas.shape, dtype=np.uint8)
canvas = cv2.add(canvas, noise)

# ── ADD RANDOM LINES ───────────────────────────────────
for _ in range(6):
    x1 = random.randint(0, cap_w)
    y1 = random.randint(0, cap_h)
    x2 = random.randint(0, cap_w)
    y2 = random.randint(0, cap_h)
    cv2.line(canvas, (x1,y1), (x2,y2), 180, 1)

# ── SAVE IMAGE ─────────────────────────────────────────
os.makedirs("public/generated", exist_ok=True)
cv2.imwrite(OUTPUT_PATH, canvas)

# ── PRINT ANSWER (Node.js reads this) ──────────────────
print(answer)