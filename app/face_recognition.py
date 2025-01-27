import os
import cv2
import numpy as np
from deepface import DeepFace
from mtcnn import MTCNN
from contextlib import contextmanager

BASE_DIR = "app/data"
DATABASE_DIR = os.path.join(BASE_DIR, "face_database")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

detector = MTCNN()

@contextmanager
def open_camera(index=0):
    cap = cv2.VideoCapture(index)
    try:
        yield cap
    finally:
        cap.release()
        cv2.destroyAllWindows()

def capture_image(prompt):
    print(f"{prompt} Press 's' to capture.")
    with open_camera() as cap:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Camera access failed.")
                break

            cv2.imshow("Capture Face", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                return frame
            elif key == ord('q'):
                return None

def register_user(name):
    user_dir = os.path.join(DATABASE_DIR, name)
    os.makedirs(user_dir, exist_ok=True)

    angles = ["straight", "left", "right", "up", "down"]
    for angle in angles:
        frame = capture_image(f"Turn {angle} for capture.")
        if frame is None:
            return False
        cv2.imwrite(os.path.join(user_dir, f"{angle}.jpg"), frame)
    
    return True

def verify_user():
    frame = capture_image("Face forward for verification.")
    if frame is None:
        return None

    temp_path = os.path.join(TEMP_DIR, "temp.jpg")
    cv2.imwrite(temp_path, frame)

    for user in os.listdir(DATABASE_DIR):
        user_dir = os.path.join(DATABASE_DIR, user)
        for file in os.listdir(user_dir):
            stored_path = os.path.join(user_dir, file)
            try:
                result = DeepFace.verify(temp_path, stored_path, model_name="Facenet", enforce_detection=False)
                if result["verified"]:
                    return user
            except:
                continue

    return None
