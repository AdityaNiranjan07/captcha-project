🔐 AI-Powered CAPTCHA System

A CAPTCHA that doesn't just ask "are you human?" — it was trained to know the difference.

Most CAPTCHAs generate a random number and check if you typed it back. This one is different. It picks real handwritten digit images from a dataset of 240,000 samples, stitches them into a distorted image with noise and rotation, and serves it as a challenge — all powered by a CNN model trained to 99.26% accuracy.
Bots can't just read a number from the DOM anymore. They'd need their own computer vision model to crack this one.

✨ What Makes This Different
Basic CAPTCHAThis ProjectMath.random() generates a numberReal handwritten images from EMNIST datasetPlain text shown to userDistorted image with noise + rotationAny bot can read it instantlyRequires computer vision to crackNo ML involvedCNN trained on 240,000 imagesAnswer visible in page sourceAnswer locked in server session only

🧠 How It Works
User visits page
      ↓
Backend runs generate.py
      ↓
5 random handwritten digit images picked from dataset
      ↓
Each digit rotated randomly (-25° to +25°)
      ↓
Stitched side by side into one image
      ↓
Noise + random lines added on top
      ↓
Image sent to frontend — answer stored in server session only
      ↓
User types what they see
      ↓
Backend compares input vs session answer
      ↓
✅ Success or ❌ Fail

🏗️ Project Structure
captcha-project/
├── server.js                  # Express backend
├── package.json
├── public/
│   ├── index.html             # Frontend UI
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
└── ml/
    ├── preprocess.py          # Cleans & resizes dataset images
    ├── train.py               # Trains the CNN model
    └── generate.py            # Generates CAPTCHA image at runtime

⚙️ ML Pipeline
Dataset: EMNIST — 240,000 grayscale handwritten digit images (0–9), 24,000 per digit
Preprocessing (preprocess.py)

Resize every image to 28×28 pixels
Gaussian blur to remove noise
Binary thresholding to clean black & white

Model Architecture (train.py)
Input (28×28 grayscale)
→ Conv2D (32 filters) + ReLU
→ MaxPooling
→ Conv2D (64 filters) + ReLU
→ MaxPooling
→ Flatten
→ Dense (128) + ReLU
→ Dropout (0.3)
→ Dense (10) + Softmax → digit 0-9
Result: 99.26% accuracy on 24,000 test images

🚀 Run It Yourself
Requirements

Node.js
Python 3.11 (TensorFlow doesn't support 3.12+)

1. Clone the repo
bashgit clone https://github.com/AdityaNiranjan07/captcha-project.git
cd captcha-project
2. Install Node dependencies
bashnpm install
3. Set up Python environment
bashpy -3.11 -m venv venv311
venv311\Scripts\activate
pip install tensorflow opencv-python numpy pillow scikit-learn
4. Get the dataset
Download the EMNIST PNG dataset from Kaggle and place it at:
captcha-project/archive/train/    ← folders 0-9, 24,000 images each
captcha-project/archive/test/     ← folders 0-9, 4,000 images each
5. Preprocess
bashpython ml/preprocess.py
6. Train the model
bashpython ml/train.py
7. Start the server
bashnode server.js
Visit http://localhost:3000

🛠️ Tech Stack

Frontend: HTML, CSS, Vanilla JavaScript
Backend: Node.js, Express, express-session
ML: Python, TensorFlow, Keras, OpenCV, NumPy
Dataset: EMNIST Balanced (Kaggle)


👤 Author
Aditya Niranjan
GitHub
