# ml/preprocess.py
import cv2
import os
import numpy as np

# ── PATHS ──────────────────────────────────────────────
RAW_DIR     = "archive/train"
CLEANED_DIR = "dataset/cleaned"
IMG_SIZE    = 28

# ── CREATE OUTPUT FOLDER ───────────────────────────────
os.makedirs(CLEANED_DIR, exist_ok=True)

# ── LOOP THROUGH EACH DIGIT FOLDER (0 to 9) ───────────
for digit in os.listdir(RAW_DIR):
    digit_path = os.path.join(RAW_DIR, digit)

    if not os.path.isdir(digit_path):
        continue

    save_path = os.path.join(CLEANED_DIR, digit)
    os.makedirs(save_path, exist_ok=True)

    print(f"Cleaning digit: {digit}")

    count = 0

    for img_file in os.listdir(digit_path):
        img_path = os.path.join(digit_path, img_file)

        # ── READ IMAGE ─────────────────────────────────
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        # ── RESIZE ────────────────────────────────────
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        # ── DENOISE ───────────────────────────────────
        img = cv2.GaussianBlur(img, (3, 3), 0)

        # ── THRESHOLD ─────────────────────────────────
        _, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

        # ── SAVE ──────────────────────────────────────
        save_file = os.path.join(save_path, f"{digit}_{count:05d}.png")
        cv2.imwrite(save_file, img)

        count += 1

    print(f"  ✓ {count} images cleaned for digit {digit}")

print("\n✅ Preprocessing complete! Cleaned images in dataset/cleaned/")