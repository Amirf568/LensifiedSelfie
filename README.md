# Lensified Selfie

**Lensified Selfie** is a fun Python tool that automatically detects a face in your image and animates sunglasses dropping onto it.

## Features

- Face and eye detection using `dlib` and OpenCV  
- Sunglasses animated using Bézier curves  
- Auto-rotation and scaling to match head tilt  
- GUI and CLI support  
- Output saved as an animated `.gif`

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lensified-selfie.git
cd lensified-selfie
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### CLI

```bash
python main.py path/to/image.jpg output.gif
```

### UI

```bash
python gui.py
```

---

## Optional: Build and Run with Docker

```bash
docker build -t lensified-selfie .
docker run --rm -v "$PWD":/app lensified-selfie python main.py path/to/input_image.jpg output.gif
```
