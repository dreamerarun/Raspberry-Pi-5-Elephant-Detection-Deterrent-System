# 🐘 Raspberry Pi 5 Elephant Detection & Deterrent System

A real-time **elephant detection and alert system** built using **Raspberry Pi 5, Pi Camera, YOLOv4, and a bee-sound deterrent mechanism**.

The system continuously captures video from the Raspberry Pi Camera, performs object detection using YOLOv4, and identifies elephants from the **COCO dataset classes**. When an elephant is detected, the system plays a bee sound through a connected audio output and controls a GPIO-connected relay/LED to provide a visual indication.

---

## 📌 Project Overview

Human-elephant conflict is a major concern in areas located near elephant habitats. This project demonstrates a low-cost computer-vision-based approach for detecting elephants in real time.

The system uses:

**Camera → Raspberry Pi 5 → YOLOv4 → Elephant Detection → Bee Sound + GPIO Alert**

### System Workflow

```text
                ┌──────────────────┐
                │   Pi Camera 2    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Raspberry Pi 5  │
                │   OpenCV + DNN   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │     YOLOv4       │
                │ Object Detection │
                └────────┬─────────┘
                         │
                  Elephant detected?
                    ┌────┴────┐
                   NO        YES
                    │          │
                    ▼          ▼
                 Continue   Bee Sound
                              +
                         GPIO Relay/LED
```

---

# 🚀 Features

* Real-time elephant detection
* YOLOv4 object detection
* Raspberry Pi Camera 2 support
* Raspberry Pi 5 compatible
* OpenCV DNN inference
* CPU-based inference
* COCO dataset class recognition
* Elephant-specific detection logic
* Bee sound playback
* GPIO-controlled relay/LED
* Real-time FPS display
* Detection bounding boxes
* Confidence scores
* Non-Maximum Suppression (NMS)
* 640 × 480 camera input
* 416 × 416 YOLO inference resolution

---

# 🧰 Hardware Requirements

## Main Components

| Component                                | Purpose                           |
| ---------------------------------------- | --------------------------------- |
| Raspberry Pi 5                           | Main processing unit              |
| Raspberry Pi Camera Module / Pi Camera 2 | Real-time image capture           |
| microSD Card                             | Raspberry Pi OS and project files |
| 5V Raspberry Pi Power Supply             | Power for Raspberry Pi 5          |
| Relay Module                             | Controls external alert/load      |
| LED                                      | Visual indication of system state |
| Speaker / USB Audio Device               | Plays bee sound                   |
| Jumper Wires                             | GPIO connections                  |
| Breadboard                               | Optional prototyping              |

### Optional Components

* External speaker
* USB sound card
* Relay-controlled buzzer
* Outdoor weatherproof enclosure
* Battery/UPS system
* Long-range camera setup
* IR illumination for night operation

---

# 🔌 GPIO Components

The provided code uses:

```python
relay_pin = 21
relay = LED(relay_pin)
```

Therefore, the control device is connected to:

**GPIO 21**

The `gpiozero` library is used to control the GPIO output.

### GPIO Concept

```text
Raspberry Pi 5
      │
      │ GPIO 21
      ▼
┌─────────────┐
│ Relay / LED │
└─────────────┘
```

> ⚠️ If a relay module is used instead of a simple LED, verify whether the relay input is active-high or active-low before connecting it. Do not connect high-power loads directly to Raspberry Pi GPIO pins.

---

# 📷 Camera Configuration

The project uses **Picamera2**.

The camera is configured with:

```python
main={"size": (640, 480)}
```

Therefore, the camera input resolution is:

**640 × 480 pixels**

The preview is disabled:

```python
picam2.start_preview(Preview.NULL)
```

This allows the camera to operate without requiring a separate camera preview window.

---

# 🤖 Object Detection Model

The project uses:

**YOLOv4**

The model consists of three important files:

```text
yolov4.cfg
yolov4.weights
coco.names
```

The code expects them at:

```text
/home/pi/Downloads/yolov4.cfg
/home/pi/Downloads/yolov4.weights
/home/pi/Downloads/coco.names
```

### Model Files

| File             | Description                  |
| ---------------- | ---------------------------- |
| `yolov4.cfg`     | YOLOv4 network configuration |
| `yolov4.weights` | Pre-trained YOLOv4 weights   |
| `coco.names`     | COCO object class names      |

The program specifically checks that the `elephant` class exists in `coco.names`.

---

# 🐘 Elephant Detection

The system performs YOLO inference on every captured frame.

The detection threshold is:

```python
confidence > 0.4
```

Non-Maximum Suppression is applied using:

```python
cv2.dnn.NMSBoxes(
    boxes,
    confidences,
    0.4,
    0.5
)
```

The elephant class is identified using:

```python
classes[class_ids[i]] == 'elephant'
```

When an elephant is detected:

```text
🐘 Elephant detected!
        │
        ├── Play bee sound
        │
        └── Blink GPIO-controlled LED/relay
```

---

# 🔊 Bee Sound Deterrent

The project uses a WAV audio file:

```text
/home/pi/Downloads/bee_converted.wav
```

The audio is loaded using:

```python
soundfile
```

and played using:

```python
sounddevice
```

### Required Audio File

```text
bee_converted.wav
```

The audio file should be a valid WAV file supported by the Raspberry Pi's configured audio device.

---

# 💡 LED / Relay Alert

The GPIO output is controlled using:

```python
from gpiozero import LED
```

GPIO 21 is initialized as:

```python
relay = LED(21)
```

The relay/LED is initially turned on:

```python
relay.on()
```

When the bee sound is playing, the program alternates the GPIO state:

```text
OFF → 0.5 sec → ON → 0.5 sec → OFF → ...
```

This creates a blinking visual indication while the deterrent sound is active.

---

# 💻 Software Requirements

## Operating System

Recommended:

**Raspberry Pi OS 64-bit**

The project is intended for:

**Raspberry Pi 5**

---

# 📦 Python Dependencies

Install the required Python packages:

```bash
sudo apt update
sudo apt install -y python3-opencv python3-picamera2
```

Install the remaining Python libraries:

```bash
pip3 install numpy sounddevice soundfile gpiozero
```

Depending on your Raspberry Pi OS configuration, you may need:

```bash
sudo apt install -y libportaudio2
```

---

# 🔧 Prerequisites

Before running the project, make sure the following are available.

### 1. Raspberry Pi 5

Verify:

```bash
cat /proc/device-tree/model
```

Expected output should contain something similar to:

```text
Raspberry Pi 5
```

---

### 2. Camera

Check that the camera is detected:

```bash
rpicam-hello
```

On some Raspberry Pi OS versions, the command may be:

```bash
libcamera-hello
```

A working camera preview indicates that the camera is properly detected.

---

### 3. Python

Check:

```bash
python3 --version
```

Python 3.x should be available.

---

### 4. OpenCV

Check:

```bash
python3 -c "import cv2; print(cv2.__version__)"
```

---

### 5. Picamera2

Check:

```bash
python3 -c "from picamera2 import Picamera2; print('Picamera2 OK')"
```

---

### 6. GPIO Zero

Check:

```bash
python3 -c "import gpiozero; print('GPIO Zero OK')"
```

---

### 7. Audio

Check the available audio devices:

```bash
aplay -l
```

You should have at least one available playback device.

---

# 📁 Recommended Project Structure

```text
elephant-detection/
│
├── elephant_detection.py
│
├── models/
│   ├── yolov4.cfg
│   ├── yolov4.weights
│   └── coco.names
│
├── audio/
│   └── bee_converted.wav
│
├── README.md
│
└── requirements.txt
```

The paths in the Python code can then be modified to match this structure.

---

# ⚙️ Model Setup

Place the YOLOv4 files in the required location.

For example:

```bash
mkdir -p ~/Downloads
```

Then ensure:

```text
~/Downloads/yolov4.cfg
~/Downloads/yolov4.weights
~/Downloads/coco.names
```

are present.

Check:

```bash
ls -lh ~/Downloads/yolov4.*
```

---

# 🔊 Audio Setup

Place the bee sound file at:

```text
/home/pi/Downloads/bee_converted.wav
```

Verify:

```bash
ls -lh /home/pi/Downloads/bee_converted.wav
```

Test audio playback independently before running the detection system.

---

# ▶️ Running the System

Run the Python program:

```bash
python3 elephant_detection.py
```

The camera window should open and display the live video stream.

When an elephant is detected, the console prints:

```text
Elephant detected!
```

The system then:

1. Plays the bee sound.
2. Starts blinking the GPIO-controlled LED/relay.
3. Displays the elephant bounding box.
4. Displays the detection confidence.

---

# 🖥️ Detection Display

The live OpenCV window displays:

```text
Elephant: 0.xx
```

along with a bounding box around the detected object.

The FPS is also displayed:

```text
FPS: xx
```

Example:

```text
┌─────────────────────────────────────┐
│                                     │
│          ┌───────────────┐          │
│          │   Elephant    │          │
│          │               │          │
│          └───────────────┘          │
│                                     │
│ FPS: 8                               │
└─────────────────────────────────────┘
```

Actual FPS depends on Raspberry Pi configuration, thermal conditions, model optimization, and background processing.

---

# ⏹️ Stop the Program

Press:

```text
q
```

inside the OpenCV display window.

The program will stop the camera and close the OpenCV window.

---

# 🔍 Detection Parameters

The current implementation uses:

| Parameter            |              Value |
| -------------------- | -----------------: |
| Camera resolution    |          640 × 480 |
| YOLO input           |          416 × 416 |
| Detection confidence |               0.40 |
| NMS threshold        |               0.50 |
| Backend              |         OpenCV DNN |
| Target               |                CPU |
| GPIO                 |                 21 |
| Sound format         |                WAV |
| Sound trigger        | Elephant detection |

---

# 🧠 Processing Pipeline

The complete software pipeline is:

```text
Pi Camera
    │
    ▼
Capture Frame
    │
    ▼
Convert Image
    │
    ▼
Resize / YOLO Blob
    │
    ▼
YOLOv4 Inference
    │
    ▼
Extract Detections
    │
    ▼
Confidence Filtering
    │
    ▼
Non-Maximum Suppression
    │
    ▼
Check Class
    │
    ├───────────────┐
    │               │
    ▼               ▼
Other Object     Elephant
    │               │
    ▼               ▼
Continue       Bee Sound
                    +
                GPIO Alert
```

---

# ⚠️ Important Hardware Safety

The Raspberry Pi GPIO pins operate at **3.3 V logic**.

Do not connect motors, high-current loads, mains-powered devices, or other high-power equipment directly to GPIO pins.

For a relay-controlled load:

```text
Raspberry Pi GPIO
       │
       ▼
 Relay Module
       │
       ▼
 External Load
```

Use an appropriate relay module/driver and an isolated external power supply when necessary.

For outdoor deployment, protect the Raspberry Pi, camera, relay, and audio electronics from:

* Rain
* Moisture
* Dust
* Direct sunlight
* High temperatures
* Electrical surges

---

# ⚡ Performance Considerations

YOLOv4 is relatively computationally demanding for a Raspberry Pi CPU.

The project therefore uses:

```python
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
```

and:

```python
input_size = 416
```

For improved performance, possible future optimizations include:

* YOLOv4-tiny
* YOLOv5/YOLOv8 nano models
* TensorFlow Lite
* ONNX Runtime
* NCNN
* OpenCV DNN optimization
* Lower camera resolution
* Frame skipping
* Hardware acceleration
* Raspberry Pi AI accelerator

---

# 🛠️ Troubleshooting

## Camera not detected

Try:

```bash
rpicam-hello
```

Check the camera connection and camera configuration.

---

## Picamera2 import error

Install:

```bash
sudo apt install python3-picamera2
```

Then test:

```bash
python3 -c "from picamera2 import Picamera2; print('OK')"
```

---

## OpenCV import error

Install:

```bash
sudo apt install python3-opencv
```

Test:

```bash
python3 -c "import cv2; print(cv2.__version__)"
```

---

## Elephant class not found

Verify:

```bash
grep -n "^elephant$" /home/pi/Downloads/coco.names
```

The file should contain:

```text
elephant
```

---

## Audio does not play

Check:

```bash
aplay -l
```

Then verify the WAV file:

```bash
file /home/pi/Downloads/bee_converted.wav
```

Also check the Raspberry Pi audio output and speaker connection.

---

## GPIO/LED does not work

Verify that the component is connected to the configured GPIO:

```text
GPIO 21
```

Test GPIO separately before running the complete application.

---

# 📊 Output

The system provides two primary outputs.

### 1. Visual Output

OpenCV displays:

* Live camera feed
* Object bounding boxes
* Object labels
* Detection confidence
* FPS

### 2. Physical Alert

When an elephant is detected:

* Bee sound is played.
* GPIO output controls the relay/LED.
* LED/relay blinks while the sound is active.

---

# 🌱 Potential Improvements

Future versions could include:

### AI Improvements

* Replace YOLOv4 with a lightweight modern detector.
* Train a dedicated elephant detection dataset.
* Improve night-time detection.
* Add elephant distance estimation.
* Add multiple-elephant tracking.
* Add false-positive filtering.
* Add temporal detection confirmation.

### Hardware Improvements

* IR/night-vision camera
* Solar power
* Battery backup
* Outdoor enclosure
* High-power outdoor speaker
* Long-range camera
* Environmental sensors

### Software Improvements

* Event logging
* Detection screenshots
* Video recording
* GPS location logging
* SMS alerts
* Telegram alerts
* Cloud dashboard
* Web-based monitoring
* Remote system health monitoring

---

# 📈 Future System Architecture

A future version could use:

```text
                  ┌──────────────┐
                  │  Pi Camera   │
                  └──────┬───────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Raspberry Pi 5  │
                │ AI Object Detect │
                └────────┬─────────┘
                         │
                  Elephant detected
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Speaker      Relay       Image
             │           │        / Video
             ▼           ▼           │
        Bee Sound    Deterrent       ▼
                                  Cloud /
                                  Mobile
```

---

# 📚 Technologies Used

* **Python**
* **OpenCV**
* **YOLOv4**
* **OpenCV DNN**
* **NumPy**
* **Picamera2**
* **Raspberry Pi 5**
* **GPIO Zero**
* **SoundDevice**
* **SoundFile**
* **COCO Dataset**

---

# 🎯 Project Objective

The primary objective of this project is to demonstrate a **low-cost real-time computer vision system for elephant detection** using edge computing.

The Raspberry Pi 5 performs the complete detection pipeline locally, allowing the system to operate without requiring continuous cloud connectivity.

When an elephant is detected, the system activates an audio and GPIO-based alert mechanism.

---

# 👨‍💻 Author

**Arun M**

B.Tech Robotics & Automation

Interested in:

* Robotics
* Computer Vision
* Autonomous Systems
* Physical AI
* Edge AI
* ROS 2
* NVIDIA Isaac
* Robot Perception

---

# ⚠️ Disclaimer

This project is an experimental/prototype implementation for elephant detection and alerting.

The bee-sound mechanism should not be considered a guaranteed elephant deterrent. Real-world deployment should involve appropriate wildlife experts, local authorities, safety assessments, and validated deterrence methods.

---

# ⭐ Acknowledgements

This project uses open-source technologies including:

* OpenCV
* YOLO
* Raspberry Pi
* Picamera2
* GPIO Zero
* NumPy
* SoundDevice
* SoundFile
* COCO dataset

---

## Quick Start

```bash
# Update system
sudo apt update

# Install system dependencies
sudo apt install -y python3-opencv python3-picamera2 libportaudio2

# Install Python dependencies
pip3 install numpy sounddevice soundfile gpiozero

# Verify camera
rpicam-hello

# Verify OpenCV
python3 -c "import cv2; print(cv2.__version__)"

# Verify Picamera2
python3 -c "from picamera2 import Picamera2; print('Picamera2 OK')"

# Run the project
python3 elephant_detection.py
```

Press **`q`** in the OpenCV window to exit.
