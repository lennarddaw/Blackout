# Blackout

A wearable real-time person tracking system using ESP32-CAM and face embeddings to analyze social interactions based on proximity and duration.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Hardware Requirements](#hardware-requirements)
4. [Software Requirements](#software-requirements)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Directory Structure](#directory-structure)
9. [Model Download](#model-download)
10. [Contributing](#contributing)
11. [License](#license)
12. [Acknowledgements](#acknowledgements)

---

## Introduction

**Blackout** is a first-person perspective (ego-view) social interaction tracker designed for educational environments. It uses an ESP32-CAM mounted on a wearable (e.g., jacket, backpack, or helmet) to capture images of your surroundings, sends them to a Raspberry Pi backend, and performs face detection and recognition via ONNX-based embeddings. New faces are prompted for naming on first sight, and subsequent interactions are logged with start/end timestamps and duration. This system enables teachers or researchers to analyze contact patterns and social bubbles among students, supporting epidemiology studies, social science research, and classroom management.

---

## Features

* **Real-Time Face Detection:** Uses OpenCV Haar cascades to detect faces in images.
* **ONNX Embedding Extraction:** Leverages a pre-trained InsightFace ONNX model (`glintr100.onnx`) for robust face embeddings.
* **On-the-Spot Enrollment:** Prompts the user to assign names to newly detected faces.
* **Local Face Database:** Stores face embeddings and names in a JSON file (`face_database.json`), no cloud storage.
* **Interaction Logging:** Records contact start and end times, duration per person, in `interactions.csv`.
* **Lightweight Dependencies:** Minimal Python packages (`flask`, `onnxruntime`, `opencv-python`, `numpy`).
* **Modular Architecture:** Separate directories for ESP32 firmware, Raspberry Pi backend, models, and utilities.

---

## Hardware Requirements

* **ESP32-CAM module** (e.g., AI-Thinker)
* **Power source** for ESP32 (5V power bank or FTDI programmer)
* **Raspberry Pi** (any model with network connectivity)
* **Optional:** Gyroscope/accelerometer (MPU6050) for stabilization, buzzer/LED for feedback

---

## Software Requirements

* **Arduino IDE** (for ESP32-CAM firmware)
* **Python 3.7+** on Raspberry Pi
* **pip** for Python package installation
* **Git** for version control

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/lennarddaw/Blackout.git
   cd Blackout
   ```

2. **Set up Python environment** (recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\Scripts\activate.bat  # Windows
   ```

3. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the ONNX model** (see [Model Download](#model-download)).

---

## Configuration

1. **ESP32-CAM (`esp32-cam/src/main.ino`):**

   * Set `ssid` and `password` to your Wi-Fi credentials.
   * Update `serverUrl` to your Raspberry Pi’s IP: `http://<PI-IP>:5000/upload`.
   * Adjust `captureInterval` (milliseconds) for snapshot frequency.

2. **Raspberry Pi (`raspberry-pi/api/server.py`):**

   * Ensure `models/glintr100.onnx` is in place.
   * Create directories:

     ```bash
     mkdir -p raspberry-pi/app/unlabeled
     ```

3. **Thresholds & Settings:**

   * Modify face-match threshold in `face_recognition.py` (default cosine similarity 0.6).

---

## Usage

1. **Start the backend** on Raspberry Pi:

   ```bash
   cd raspberry-pi/api
   python server.py
   ```

2. **Flash and run** the ESP32-CAM firmware (`main.ino`) via Arduino IDE.

3. **Monitor console**:

   * New faces trigger a prompt: enter a name.
   * Known faces print recognized names.

4. **Inspect logs**:

   * `raspberry-pi/app/face_database.json` – stored embeddings and names.
   * `raspberry-pi/app/logs/interactions.csv` – interaction records.

---

## Directory Structure

```plaintext
Blackout/
├── esp32-cam/
│   └── src/
│       └── main.ino             # ESP32-CAM firmware
├── raspberry-pi/
│   ├── api/
│   │   └── server.py            # Flask image upload & naming API
│   └── app/
│       ├── face_recognition.py  # ONNX embedding & matching logic
│       ├── face_database.json   # Saved embeddings + names
│       └── logs/
│           └── interactions.csv # Contact logs
├── models/
│   └── glintr100.onnx           # Face embedding model (download separately)
├── utils/
│   ├── embedding_tools.py       # Helper functions
│   └── logger.py                # Logging utilities
├── requirements.txt             # Python dependencies
├── .gitignore                   # Ignored files & folders
└── LICENSE                      # MIT License
```

---

## Model Download

The ONNX model exceeds GitHub’s 100 MB limit and must be downloaded manually:

```bash
mkdir -p models
wget https://github.com/deepinsight/insightface/releases/download/v1.0/glintr100.onnx -O models/glintr100.onnx
```

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m "Add YourFeature"`.
4. Push to branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

* [InsightFace](https://github.com/deepinsight/insightface) for the face embedding models.
* [Espressif ESP32-CAM](https://github.com/espressif/esp32-camera)
* [ONNX Runtime](https://www.onnxruntime.ai/)

---

**Enjoy tracking your social bubbles!**
