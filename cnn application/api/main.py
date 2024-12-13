from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

from tensorflow.keras.models import load_model

model_paths = {
    "big_drop_16": "./../../models/Bigger Drop/16.keras",
    "big_drop_32": "./../../models/Bigger Drop/32.keras",

    "custom_8": "./../../models/custom cnn/CustomFirst_8.keras",
    "custom_16": "./../../models/custom cnn/CustomFirst_16.keras",
    "custom_32": "./../../models/custom cnn/CustomFirst_32.keras",
    "custom_64": "./../../models/custom cnn/CustomFirst_64.keras",

    "base_model_8": "./../../models/Base Model/8.keras",
    "base_model_16": "./../../models/Base Model/16.keras",
    "base_model_32": "./../../models/Base Model/32.keras",

    "dropout_b_16": "./../../models/Dropout B/16.keras",
    "dropout_b_32": "./../../models/Dropout B/32.keras",

    "a_lot_of_dropout_16": "./../../models/Alot of Drop/16.keras",
    "a_lot_of_dropout_32": "./../../models/Alot of Drop/32.keras",

    "dense_deep_16": "./../../models/Dense Deep/16.keras",
    "dense_deep_32": "./../../models/Dense Deep/32.keras",

    "efficientnet_scratch16": "./../../models/scratch/EfficientNet/EfficientNet_16.keras",
    "efficientnet_scratch32": "./../../models/scratch/EfficientNet/EfficientNet_32.keras",

    "inception_scratch16": "./../../models/scratch/InceptionNet/InceptionNet_16.keras",

    "mobilenet_scratch16": "./../../models/scratch/MobileNet/MobileNet_16.keras",
    "mobilenet_scratch32": "./../../models/scratch/MobileNet/MobileNet_32.keras",
    "mobilenet_scratch64": "./../../models/scratch/MobileNet/MobileNet_64.keras",

    "resnet_scratch8": "./../../models/scratch/ResNet/ResNet_8.keras",
    "resnet_scratch16": "./../../models/scratch/ResNet/ResNet_16.keras",
    "resnet_scratch32": "./../../models/scratch/ResNet/ResNet_32.keras",
    "resnet_scratch64": "./../../models/scratch/ResNet/ResNet_64.keras",

    "densenet_non_trainable_8": "./../../models/transfer learning/base_model not trainable/DenseNet21/8.keras",
    "densenet_non_trainable_16": "./../../models/transfer learning/base_model not trainable/DenseNet21/16.keras",
    "densenet_non_trainable_32": "./../../models/transfer learning/base_model not trainable/DenseNet21/32.keras",

    "efficientnet_non_trainable_8": "./../../models/transfer learning/base_model not trainable/EfficientNetv20B0/8.keras",
    "efficientnet_non_trainable_16": "./../../models/transfer learning/base_model not trainable/EfficientNetv20B0/16.keras",
    "efficientnet_non_trainable_32": "./../../models/transfer learning/base_model not trainable/EfficientNetv20B0/32.keras",

    "inception_non_trainable_8": "./../../models/transfer learning/base_model not trainable/InceptionNetv3/8.keras",
    "inception_non_trainable_16": "./../../models/transfer learning/base_model not trainable/InceptionNetv3/16.keras",
    "inception_non_trainable_32": "./../../models/transfer learning/base_model not trainable/InceptionNetv3/32.keras",

    "mobilenet_non_trainable_8": "./../../models/transfer learning/base_model not trainable/MobileNetv3Large/8.keras",
    "mobilenet_non_trainable_16": "./../../models/transfer learning/base_model not trainable/MobileNetv3Large/16.keras",
    "mobilenet_non_trainable_32": "./../../models/transfer learning/base_model not trainable/MobileNetv3Large/32.keras",

    "resnet_non_trainable_8": "./../../models/transfer learning/base_model not trainable/ResNet50v2/8.keras",
    "resnet_non_trainable_16": "./../../models/transfer learning/base_model not trainable/ResNet50v2/16.keras",
    "resnet_non_trainable_32": "./../../models/transfer learning/base_model not trainable/ResNet50v2/32.keras",

    "efficientnet_trainable_8": "./../../models/transfer learning/base_model trainable/EfficientNetv20B0/8.keras",
    "efficientnet_trainable_16": "./../../models/transfer learning/base_model trainable/EfficientNetv20B0/16.keras",
    "efficientnet_trainable_32": "./../../models/transfer learning/base_model trainable/EfficientNetv20B0/32.keras",
    "efficientnet_trainable_64": "./../../models/transfer learning/base_model trainable/EfficientNetv20B0/64.keras",

    "inceptionnet_trainable_8": "./../../models/transfer learning/base_model trainable/InceptionNetv3/8.keras",
    "inceptionnet_trainable_16": "./../../models/transfer learning/base_model trainable/InceptionNetv3/16.keras",
    "inceptionnet_trainable_32": "./../../models/transfer learning/base_model trainable/InceptionNetv3/32.keras",
    "inceptionnet_trainable_64": "./../../models/transfer learning/base_model trainable/InceptionNetv3/64.keras",

    "mobilenet_trainable_8": "./../../models/transfer learning/base_model trainable/MobileNetv3Large/8.keras",
    "mobilenet_trainable_16": "./../../models/transfer learning/base_model trainable/MobileNetv3Large/16.keras",
    "mobilenet_trainable_32": "./../../models/transfer learning/base_model trainable/MobileNetv3Large/32.keras",
    "mobilenet_trainable_64": "./../../models/transfer learning/base_model trainable/MobileNetv3Large/64.keras",

    "resnet_trainable_8": "./../../models/transfer learning/base_model trainable/ResNet50v2/8.keras",
    "resnet_trainable_16": "./../../models/transfer learning/base_model trainable/ResNet50v2/16.keras",
    "resnet_trainable_32": "./../../models/transfer learning/base_model trainable/ResNet50v2/32.keras",
    "resnet_trainable_64": "./../../models/transfer learning/base_model trainable/ResNet50v2/64.keras",
}

model_path = model_paths['resnet_non_trainable_16']

model = tf.keras.models.load_model(model_path)
print(f"Model Loaded Successfully.")


class_names = [
    'Green Light',
    'Red Light',
    'Speed Limit 10',
    'Speed Limit 100',
    'Speed Limit 110',
    'Speed Limit 120',
    'Speed Limit 20',
    'Speed Limit 30',
    'Speed Limit 40',
    'Speed Limit 50',
    'Speed Limit 60',
    'Speed Limit 70',
    'Speed Limit 80',
    'Speed Limit 90',
    'Stop'
]



app = FastAPI()

origins = [
    "http://localhost",  
    "http://localhost:3000"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def read_file_as_image(data) -> np.array:
    img = np.array(Image.open(BytesIO(data)))
    return img



@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    image_batch = np.expand_dims(image, 0)
    predictions = model.predict(image_batch)

    predicted_class = class_names[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    return {
        "class": predicted_class,
        "confidence": float(confidence),
    }



if __name__ == "__main__":
    uvicorn.run(app, host= 'localhost', port = 8000)
