# Traffic Sign Detection

## Overview

This project is a comprehensive solution for traffic sign detection, featuring:
- A web application for interactive inference
- Model inference testing system
- Neural network training scripts
- YOLO prediction capabilities

The project is designed to provide a seamless workflow for model training, multi-image inference, and real-time predictions using cameras or video streams.

## Prerequisites

Before getting started, ensure you have the following installed:
- Python 3.8+
- Node.js 14+
- npm (Node Package Manager)

## Installation

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/traffic-sign-detection.git
   cd traffic-sign-detection
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   cd backend/API
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   cd src
   npm start
   ```

## Project Structure

- `cnn_application/api/`: Contains the server-side code and API
- `cnn_application/frontend/`: Web application source code
- `training/`: Jupyter notebooks for model training
- `models/`: Saved machine learning models
- `model_inference/`: Notebooks for model evaluation and testing

## Training

Training notebooks are located in the `training/` directory. These notebooks provide scripts and guidelines for:
- Data preprocessing
- Model architecture design
- Training procedures
- Model evaluation

## Model Inference

### Image Inference

1. Navigate to the URL [localhos:](http://localhost:3000/)
2. Select images from the dataset folder
3. Run inference on CNN or YOLO models

### Camera and Video Inference

The project supports real-time traffic sign detection using:
- Live camera feeds
- Pre-recorded video files

## Evaluation

Comprehensive model evaluation notebooks are available in the `model_inference/` directory, supporting:
- Multi-file inference
- Performance metrics
- Visualization of detection results
