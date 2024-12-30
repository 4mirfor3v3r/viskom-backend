import os

import onnxruntime
from fastapi import FastAPI, UploadFile, File
from starlette.responses import JSONResponse
import numpy as np
from PIL import Image, ImageDraw
from fastapi.staticfiles import StaticFiles

app = FastAPI()
loaded_model = onnxruntime.InferenceSession("FasterRCNN_MobileNetV3_320FPN_large_0.881_dynamic.onnx")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post('/detect-image')
def detect_image(image: UploadFile = File(...)):
    originalImg = Image.open(image.file)
    img = np.array(originalImg)
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    img = img.astype(np.float32)
    img = img / 255.0

    result = []
    output = loaded_model.run(None, {'images': img})
    for i in range(len(output)):
        boxes = output[0][i]
        scores = output[2][i]
        labels = output[1][i]
        if scores > 0.6:
            result.append({"box": boxes.tolist(), "conf_score": float(scores), "label": float(labels)})
            # draw bbox
            draw = ImageDraw.Draw(originalImg)
            draw.rectangle(boxes, outline="red", width=3)
            # draw confidence score each box
            draw.text((boxes[0], boxes[1]), f"Conf: {scores:.2f}", fill="blue")
    # save image and generate image link
    originalImg.save("static/output.jpg")

    #generate link
    link = f"{str(os.environ.get('BASE_URL', '0.0.0.0'))}/static/output.jpg"

    return JSONResponse(status_code=200, content={"success": True, "data": result, "image_link": link})