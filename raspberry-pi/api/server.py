from flask import Flask, request
import cv2
import numpy as np
import os
from datetime import datetime
import uuid

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from app.face_recognition import (
    detect_face_opencv,
    preprocess_face,
    get_embedding,
    identify_face,
    save_new_face,
    check_for_new_face,
)

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'app', 'unlabeled')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    # 1) Multipart/form-data Upload?
    if 'image' in request.files:
        file = request.files['image']
        img_data = file.read()
    # 2) Raw JPEG in Body?
    elif request.content_type and 'image/jpeg' in request.content_type:
        img_data = request.get_data()
    else:
        return "No image provided", 400

    # dekodiere JPEG
    image = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        return "Cannot decode image", 400

    # Gesichtserkennung mit OpenCV
    faces = detect_face_opencv(image)
    print(f"{len(faces)} face(s) detected.")

    for (x, y, w, h) in faces:
        bbox = (x, y, x + w, y + h)
        face_input = preprocess_face(image, bbox)
        embedding = get_embedding(face_input)
        name = identify_face(embedding)

        if name is None:
            # neues Gesicht: Vorschau speichern + Namen abfragen
            filename = f"{datetime.now():%Y%m%d_%H%M%S}_{uuid.uuid4().hex[:6]}.jpg"
            path = os.path.join(UPLOAD_DIR, filename)
            cv2.imwrite(path, image)
            print(f"New face! Preview saved to {path}")
            name = input("Please enter name: ")
            save_new_face(name, embedding)
            print(f"Saved new face as {name}")
        else:
            print(f"Known face: {name}")

    return "OK", 200

if __name__ == "__main__":
    # läuft auf Port 5000, Route /upload
    app.run(host="0.0.0.0", port=5000)
