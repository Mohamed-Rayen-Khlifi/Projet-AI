import os
import shutil
import os
import tensorflow as tf
import os
from roboflow import Roboflow
from tensorflow.keras import models, layers
import matplotlib.pyplot as plt
import pandas as pd
import shutil

classes = {
    '0': 'Green Light',
    '1': 'Red Light',
    '2': 'Speed Limit 10',
    '3': 'Speed Limit 100',
    '4': 'Speed Limit 110',
    '5': 'Speed Limit 120',
    '6': 'Speed Limit 20',
    '7': 'Speed Limit 30',
    '8': 'Speed Limit 40',
    '9': 'Speed Limit 50',
    '10': 'Speed Limit 60',
    '11': 'Speed Limit 70',
    '12': 'Speed Limit 80',
    '13': 'Speed Limit 90',
    '14': 'Stop'
}

def organize_images_by_class(image_dir, label_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Get all image filenames (without extension) in the image directory
    image_files = {os.path.splitext(f)[0]: f for f in os.listdir(image_dir)}

    # Iterate through label files in the label directory
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

    for label_file in label_files:
        label_path = os.path.join(label_dir, label_file)
        image_name = os.path.splitext(label_file)[0]

        # Check if a corresponding image exists
        if image_name not in image_files:
            print(f"Warning: No image found for label {label_file}. Skipping.")
            continue

        # Resolve the full image path
        image_path = os.path.join(image_dir, image_files[image_name])

        with open(label_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                print(f"Warning: {label_file} is empty. Skipping.")
                continue

            first_class_id = classes[lines[0].split()[0]]

        class_dir = os.path.join(output_dir, first_class_id)
        os.makedirs(class_dir, exist_ok=True)

        # Copy the image to the appropriate directory
        shutil.copy(image_path, class_dir)

    print("Organizing completed successfully.")


classes = {
    '0': 'Green Light',
    '1': 'Red Light',
    '2': 'Speed Limit 10',
    '3': 'Speed Limit 100',
    '4': 'Speed Limit 110',
    '5': 'Speed Limit 120',
    '6': 'Speed Limit 20',
    '7': 'Speed Limit 30',
    '8': 'Speed Limit 40',
    '9': 'Speed Limit 50',
    '10': 'Speed Limit 60',
    '11': 'Speed Limit 70',
    '12': 'Speed Limit 80',
    '13': 'Speed Limit 90',
    '14': 'Stop'
}

def organize_images_by_class(image_dir, label_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Get all image filenames (without extension) in the image directory
    image_files = {os.path.splitext(f)[0]: f for f in os.listdir(image_dir)}

    # Iterate through label files in the label directory
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

    for label_file in label_files:
        label_path = os.path.join(label_dir, label_file)
        image_name = os.path.splitext(label_file)[0]

        # Check if a corresponding image exists
        if image_name not in image_files:
            print(f"Warning: No image found for label {label_file}. Skipping.")
            continue

        # Resolve the full image path
        image_path = os.path.join(image_dir, image_files[image_name])

        with open(label_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                print(f"Warning: {label_file} is empty. Skipping.")
                continue

            first_class_id = classes[lines[0].split()[0]]

        class_dir = os.path.join(output_dir, first_class_id)
        os.makedirs(class_dir, exist_ok=True)

        # Copy the image to the appropriate directory
        shutil.copy(image_path, class_dir)

    print("Organizing completed successfully.")



rf = Roboflow(api_key="0VZYY90r4l05ICemwLNZ")
project = rf.workspace("selfdriving-car-qtywx").project("self-driving-cars-lfjou")
version = project.version(6)
dataset = version.download("yolov8")

input_dir = '/kaggle/working/Self-Driving-Cars-6/test'

image_test2_directory = '/kaggle/working/Self-Driving-Cars-6/test/images'
label_test2_directory = '/kaggle/working/Self-Driving-Cars-6/test/labels'
output_test2_directory = "./test2"

!rm -rf test2

organize_images_by_class(image_test2_directory, label_test2_directory, output_test2_directory)


test2_data = tf.keras.utils.image_dataset_from_directory(
    output_test2_directory,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    shuffle=True
)

model_8.evaluate(test2_data)