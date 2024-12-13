import os
import cv2
from ultralytics import YOLO

# Set video directory
VIDEOS_DIR = os.path.join('.', 'videos')

model_path = '../models/yolo/best_yolo/best.pt'
model_name = YOLO(model_path)  # Load the custom model


# Get video paths from input
video_path = os.path.join(VIDEOS_DIR, input("File Name without the extension: ") + '.mp4')
video_path_out = '{}_out.mp4'.format(video_path[:len(video_path)-4])

# Initialize video capture and output
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))


model = model_name

# Set detection threshold
threshold = 0.2

# Define colors for each class
# Assuming class 0 is for light blue, class 1 is for pink, and class 2 is for white
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

# Process each frame of the video
while ret:
    results = model(frame)[0]  # Perform detection on the frame

    # Iterate through each detected box
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:  # Only process boxes above the threshold
            class_id = int(class_id)  # Class index
            color = colors[class_id]  # Get color for the class

            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)

            # Display class label with confidence score
            label = f"{model.names[class_id].upper()} {score:.2f}"
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3, cv2.LINE_AA)

    # Write the frame with detections to the output video
    out.write(frame)
    ret, frame = cap.read()

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
