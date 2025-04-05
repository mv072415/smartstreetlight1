import sys
sys.path.append("C:/Users/kirlo/Documents/smartstreetlight")
import cv2
import numpy as np
from weather_api import get_weather  # ✅ Import Weather API Function

# Load AI model for object detection
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "mobilenet_iter_73000.caffemodel")

# Define object categories
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

# Open the webcam (or use a video file)
cap = cv2.VideoCapture(0)  

while True:
    ret, frame = cap.read()
    if not ret:
        break  

    # Prepare the frame for AI detection
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # **🔹 Get Current Weather Condition** 
    weather_condition = get_weather()  
    print(f"Weather: {weather_condition}")  

    # **🌞 Adjust Brightness Based on Weather & Object Detection**
    brightness = 30  # Default low brightness

    if weather_condition in ["Rain", "Fog", "Snow"]:  
        brightness = 80  # Increase brightness during bad weather

    # Loop through detected objects
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]

            # If a person, car, or bus is detected, increase brightness
            if label in ["person", "car", "bus"]:
                brightness = 100  # Full brightness for safety

            # Get bounding box coordinates
            box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
            (x1, y1, x2, y2) = box.astype("int")

            # Draw detection box & label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            text = f"{label}: {int(confidence * 100)}%"
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # **🔆 Display Brightness Level**
    cv2.putText(frame, f"Brightness: {brightness}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("Smart Street Lighting", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 
