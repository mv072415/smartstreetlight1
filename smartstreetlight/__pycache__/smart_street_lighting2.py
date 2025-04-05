import cv2
import numpy as np

# Load Caffe model
prototxt_path = 'model/deploy.prototxt'
model_path = 'model/mobilenet_iter_73000.caffemodel'

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Class labels for MobileNet SSD
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

def process_image(image_path):
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]

    # Prepare blob for model
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            label = CLASSES[idx]
            if label in ["person", "car", "bus", "bicycle", "motorbike"]:
                return "LIGHT ON 🚦"

    return "LIGHT OFF 🌙"
