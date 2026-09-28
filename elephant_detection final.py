import cv2
import numpy as np
import time
from picamera2 import Picamera2, Preview
import sounddevice as sd
import soundfile as sf  # Import the soundfile library to read WAV files
from gpiozero import LED

# Load YOLO model configuration and weights
model_cfg = r"/home/pi/Downloads/yolov4.cfg"
model_weights = r"/home/pi/Downloads/yolov4.weights"
class_names = r"/home/pi/Downloads/coco.names"

# Load the names of the classes
with open(class_names, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Check if 'elephant' is in the class list
if 'elephant' not in classes:
    print("Elephant class not found in the coco.names file.")
    exit()

# Load the network
net = cv2.dnn.readNet(model_weights, model_cfg)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Define input size for the model
input_size = 416  # Reduced input size for faster processing

# Initialize Pi Camera
picam2 = Picamera2()
picam2.start_preview(Preview.NULL)
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}, raw={"size": (640, 480)}))  # Set resolution
picam2.start()

# Load the bee sound file using soundfile
bee_sound_path = "/home/pi/Downloads/bee_converted.wav"  # Replace with the correct path to the sound file
bee_sound, sample_rate = sf.read(bee_sound_path)  # Read the sound file using soundfile

# Define GPIO pin for relay (LED)
relay_pin = 21
relay = LED(relay_pin)

# Initially turn on the relay (LED) to indicate the system is active
relay.on()

# Real-time detection loop
fps = 0
frame_count = 0
start_time = time.time()

# Define output layer names
output_layers = net.getUnconnectedOutLayersNames()

# To keep track of whether an elephant was detected
elephant_detected = False

# To track sound play time and reset detection
sound_play_start_time = None
sound_play_duration = 10  # 10 minutes in seconds
sound_playing = False  # Track sound playing status

def play_sound_and_blink():
    global sound_playing

    if not sound_playing:
        sound_playing = True
        print("Playing sound and starting LED blink.")
        sd.play(bee_sound, sample_rate )  # Play the bee sound

        # Blink LED while sound is playing
        while sound_playing:
            # Blink the LED (assuming LED is connected to relay)
            relay.off()  # Turn off the relay (LED) as part of the blinking pattern
            time.sleep(0.5)  # LED off for 0.5 seconds
            relay.on()  # Turn on the relay (LED)
            time.sleep(0.5)  # LED on for 0.5 seconds

            # Check if the sound has finished playing
            if not sd.get_stream().active:  # Check if the sound is still playing
                sound_playing = False  # Stop the loop if sound has finished
                print("Sound finished playing. Stopping LED blink.")
                relay.on()  # Ensure LED is on after sound finishes

# Main loop
while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()
    if frame is None:
        print("Error: Failed to capture frame.")
        break

    # Convert frame to RGB if necessary
    if frame.shape[2] == 4:  # Check if there are 4 channels (RGBA)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB if needed

    height, width = frame.shape[:2]

    # Create a blob from the frame
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (input_size, input_size), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward pass to get detections
    outputs = net.forward(output_layers)

    # Initialize lists to store detection results
    boxes = []
    confidences = []
    class_ids = []

    # Process detections
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.4:  # Confidence threshold
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.5)

    # Track if elephant is detected
    elephant_detected = False

    if len(indices) > 0:
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box
            label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
            color = (0, 255, 0) if classes[class_ids[i]] == 'elephant' else (0, 0, 255)

            # Check if the detected object is an elephant
            if classes[class_ids[i]] == 'elephant' and not elephant_detected:
                elephant_detected = True  # Mark as elephant detected
                print("Elephant detected!")
                play_sound_and_blink()  # Play sound and blink the LED

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Calculate and display FPS
    frame_count += 1
    if time.time() - start_time >= 1:  # Update every second
        fps = frame_count
        frame_count = 0
        start_time = time.time()

    # Display FPS on the frame
    cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Elephant Detection', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
picam2.stop()
cv2.destroyAllWindows()

