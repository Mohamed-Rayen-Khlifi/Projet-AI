import os
import cv2
from ultralytics import YOLO

#Execute with 3.10 python
# Load the YOLO model

model_path = '../models/yolo/best_yolo/last.pt'
model = YOLO(model_path)  # Load the custom model

# Set detection threshold
threshold = 0.2  # Adjust the detection threshold if needed

# Define colors for each class (Assuming class 0 is for light blue, 1 for pink, 2 for white)
colors = {
    0: (173, 216, 230),  # Light Blue
    1: (255, 192, 203),  # Pink
    2: (255, 255, 255),  # White
    3: (144, 238, 144),  # Light Green
    4: (255, 165, 0),    # Orange
    5: (221, 160, 221),  # Plum
    6: (255, 228, 181),  # Light Peach
    7: (240, 230, 140),  # Khaki
    8: (255, 250, 205),  # Lemon Chiffon
    9: (135, 206, 250),  # Sky Blue
    10: (255, 105, 180), # Hot Pink
    11: (255, 99, 71),   # Tomato
    12: (152, 251, 152), # Pale Green
    13: (70, 130, 180),  # Steel Blue
    14: (210, 180, 140)  # Tan
}

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use '0' to access the default camera

if not cap.isOpened():
    print("Error: Cannot open camera.")
    exit()

# Process each frame from the camera feed
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    # Perform detection on the frame
    results = model(frame)[0]

    # Iterate through each detected box
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:  # Only process boxes above the threshold
            class_id = int(class_id)  # Class index
            color = colors.get(class_id, (0, 255, 0))  # Get color for the class, default to green

            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)

            # Display class label with confidence score
            label = f"{model.names[class_id].upper()} {score:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2, cv2.LINE_AA)

    # Show the frame with the detection
    cv2.imshow('Real-time YOLO Detection', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()