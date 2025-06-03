import onnxruntime
import numpy as np
import cv2
import json
import os

DB_PATH = "face_database.json"
MODEL_PATH = "models/glintr100.onnx"
INPUT_SIZE = (112, 112)

session = onnxruntime.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])


if os.path.exists(DB_PATH):
    with open(DB_PATH, "r") as f:
        known_faces = json.load(f)
else:
    known_faces = []

def preprocess_face(img, bbox):
    x1, y1, x2, y2 = bbox
    face = img[y1:y2, x1:x2]
    face = cv2.resize(face, INPUT_SIZE)
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = face.astype(np.float32) / 255.0
    face = np.transpose(face, (2, 0, 1))[None, ...]
    return face

def get_embedding(face_input):
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: face_input})[0]
    return output[0] / np.linalg.norm(output[0])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def identify_face(embedding, threshold=0.6):
    for entry in known_faces:
        sim = cosine_similarity(embedding, entry["embedding"])
        if sim > threshold:
            return entry["name"]
    return None

def save_new_face(name, embedding):
    known_faces.append({
        "name": name,
        "embedding": embedding.tolist()
    })
    with open(DB_PATH, "w") as f:
        json.dump(known_faces, f, indent=2)

def check_for_new_face(name, embedding):
    existing_face = identify_face(embedding)
    if existing_face is None:
        save_new_face(name, embedding)
        return f"New face detected and saved: {name}"
    else:
        return f"Face already exists in database: {existing_face}"

def detect_face_opencv(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    return faces
