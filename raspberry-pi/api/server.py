from flask import Flask, request
import cv2
import numpy as np
import os
from datetime import datetime
import uuid

from app.face_recognition import (
    detect_face_opencv,
    preprocess_face,
    get_embedding,
    identify_face,
    save_new_face
)

app = Flask(__name__)
UPLOAD_DIR = "app/unlabeled"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    if not file:
        return "No image provided", 400

    # Lade und dekodiere das Bild
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Finde Gesichter mit OpenCV
    faces = detect_face_opencv(image)
    print(f"{len(faces)} Gesicht(er) erkannt.")

    for (x, y, w, h) in faces:
        bbox = (x, y, x + w, y + h)
        try:
            face_input = preprocess_face(image, bbox)
            embedding = get_embedding(face_input)
        except Exception as e:
            print(f"Fehler beim Verarbeiten des Gesichts: {e}")
            continue

        name = identify_face(embedding)
        if name is None:
            # Neues Gesicht erkannt → Speichern & Namen abfragen
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.jpg"
            path = os.path.join(UPLOAD_DIR, filename)
            cv2.imwrite(path, image)
            print(f"Neues Gesicht erkannt. Vorschau gespeichert: {path}")
            name = input("Bitte gib den Namen ein: ")
            save_new_face(name, embedding)
            print(f"Gesicht gespeichert als {name}")
        else:
            print(f"Bekanntes Gesicht erkannt: {name}")

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
