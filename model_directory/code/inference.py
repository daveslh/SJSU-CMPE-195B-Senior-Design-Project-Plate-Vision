import torch
from PIL import Image
import numpy as np
import json
from io import BytesIO

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/octet-stream':
        image_data = request_body
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}. Expected raw bytes.")

    image = Image.open(BytesIO(image_data)).resize((640, 640))
    image_array = np.array(image) / 255.0
    image_array = np.transpose(image_array, (2, 0, 1))
    image_array = np.expand_dims(image_array, axis=0).astype(np.float32)

    return torch.tensor(image_array), image

def predict_fn(input_data_tuple, model):
    input_data, original_image = input_data_tuple
    model.eval()
    
    with torch.no_grad():
        predictions = model(input_data)

    predictions = predictions[0]
    confidence_threshold = 0.5
    positive_predictions = predictions[predictions[:, 4] > confidence_threshold]

    if positive_predictions.size == 0:
        return {"message": "No objects detected", "confidence": 0.0, "bounding_box": [], "class_id": None}

    best_prediction = positive_predictions[positive_predictions[:, 4].argmax()]
    x1, y1, x2, y2, conf, cls = best_prediction.tolist()

    if int(cls) == 0:
        # Crop and encode the cropped image as a Latin-1 string
        cropped_image = original_image.crop((x1, y1, x2, y2))
        buffered_cropped = BytesIO()
        cropped_image.save(buffered_cropped, format="JPEG")
        cropped_image_latin1 = buffered_cropped.getvalue().decode('latin1')

        # Encode the original image as a Latin-1 string
        buffered_original = BytesIO()
        original_image.save(buffered_original, format="JPEG")
        original_image_latin1 = buffered_original.getvalue().decode('latin1')

        result = {
            "inference_result": {
                "confidence": conf,
                "bounding_box": [x1, y1, x2, y2],
                "class_id": int(cls)
            },
            "cropped_image": cropped_image_latin1,
            "original_image": original_image_latin1  # Include original image as Latin-1 string
        }

        return result

    return {"message": f"No objects were detected that were of class id {int(cls)}"}

def output_fn(prediction, content_type):
    if content_type == 'application/json':
        return json.dumps(prediction), content_type
    else:
        raise ValueError(f"Unsupported content type: {content_type}")
