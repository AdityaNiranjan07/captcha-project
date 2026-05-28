# ml/train.py
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import cv2
import os
from sklearn.utils import shuffle

# ── PATHS ──────────────────────────────────────────────
CLEANED_DIR = "dataset/cleaned"
MODEL_PATH  = "model/captcha_model.keras"
IMG_SIZE    = 28

os.makedirs("model", exist_ok=True)

# ── LOAD IMAGES ────────────────────────────────────────
images = []
labels = []

print("Loading cleaned images...")

for digit in range(10):
    digit_path = os.path.join(CLEANED_DIR, str(digit))
    if not os.path.isdir(digit_path):
        print(f"  ⚠ Folder missing: {digit_path}")
        continue
    count = 0
    for img_file in os.listdir(digit_path):
        img_path = os.path.join(digit_path, img_file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        images.append(img)
        labels.append(digit)
        count += 1
    print(f"  ✓ Digit {digit}: {count} images loaded")

print(f"\nTotal images: {len(images)}")

# ── PREPARE DATA ───────────────────────────────────────
images = np.array(images, dtype=np.float32).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
images = images / 255.0
labels = np.array(labels, dtype=np.int32)

# ── SHUFFLE ────────────────────────────────────────────
images, labels = shuffle(images, labels, random_state=42)

# verify label distribution
print(f"Label distribution: {np.bincount(labels)}")

# ── SPLIT ──────────────────────────────────────────────
split = int(len(images) * 0.9)
x_train, x_test = images[:split], images[split:]
y_train, y_test = labels[:split], labels[split:]

print(f"Training: {len(x_train)} | Testing: {len(x_test)}")

# ── BUILD MODEL ────────────────────────────────────────
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ── TRAIN ──────────────────────────────────────────────
print("\nTraining model...")
model.fit(
    x_train, y_train,
    epochs=5,
    batch_size=64,
    validation_data=(x_test, y_test)
)

# ── EVALUATE ───────────────────────────────────────────
loss, acc = model.evaluate(x_test, y_test)
print(f"\n✅ Model accuracy: {acc*100:.2f}%")

# ── SAVE ───────────────────────────────────────────────
model.save(MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH}")