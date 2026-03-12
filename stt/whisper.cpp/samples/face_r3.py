import cv2
import numpy as np
import os
import random
import subprocess
import sys
import urllib.request
from picamera2 import Picamera2

os.makedirs("stranger", exist_ok=True)

KNOWN_DIR = "./images"
WATCH_FILE = "watch.txt"
SIMILARITY_THRESHOLD = 0.35
VOICE_LOOP_SCRIPT = os.path.join(os.path.dirname(__file__), "voice_loop5.py")

YUNET_MODEL = "face_detection_yunet_2023mar.onnx"
SFACE_MODEL = "face_recognition_sface_2021dec.onnx"

YUNET_URL = ("/home/charles/ai-pet/stt/whisper.cpp/samples/face_r3/face_detection_yunet_2023mar.onnx")
 
SFACE_URL = ("/home/charles/ai-pet/stt/whisper.cpp/samples/face_r3/face_recognition_sface_2021dec.onnx")


def ensure_model(path, url):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return
    print(f"Downloading {path} ...")
    urllib.request.urlretrieve(url, path)


def get_largest_face(detector, frame):
    detector.setInputSize((frame.shape[1], frame.shape[0]))
    _, faces = detector.detect(frame)
    if faces is None or len(faces) == 0:
        return None
    return max(faces, key=lambda item: item[2] * item[3])


def extract_feature(detector, recognizer, frame):
    face = get_largest_face(detector, frame)
    if face is None:
        return None
    aligned = recognizer.alignCrop(frame, face)
    return recognizer.feature(aligned)


def load_known_faces(detector, recognizer):
    names = []
    features = []

    if not os.path.isdir(KNOWN_DIR):
        return names, features

    for filename in os.listdir(KNOWN_DIR):
        path = os.path.join(KNOWN_DIR, filename)
        if not os.path.isfile(path):
            continue

        image = cv2.imread(path)
        if image is None:
            continue

        feature = extract_feature(detector, recognizer, image)
        if feature is None:
            continue

        names.append(os.path.splitext(filename)[0])
        features.append(feature)

    return names, features


def recognize_name(recognizer, query_feature, known_names, known_features):
    if query_feature is None or not known_features:
        return "human", 0.0

    best_name = "human"
    best_score = -1.0

    for name, known_feature in zip(known_names, known_features):
        score = recognizer.match(query_feature, known_feature, cv2.FaceRecognizerSF_FR_COSINE)
        if score > best_score:
            best_score = score
            best_name = name

    if best_score >= SIMILARITY_THRESHOLD:
        return best_name, best_score
    return "human", best_score


def main():
    ensure_model(YUNET_MODEL, YUNET_URL)
    ensure_model(SFACE_MODEL, SFACE_URL)

    detector = cv2.FaceDetectorYN.create(YUNET_MODEL, "", (320, 240), 0.8, 0.3, 5000)
    recognizer = cv2.FaceRecognizerSF.create(SFACE_MODEL, "")

    known_names, known_features = load_known_faces(detector, recognizer)
    print(f"Loaded {len(known_names)} known faces")

    try:
        picam2 = Picamera2()    
    except RuntimeError as e:
        print(f"Camera unavailable: {e}")
        print("Another process is using the camera. Stop it and retry.")
        return
    config = picam2.create_video_configuration(main={"size": (640, 480), "format": "BGR888"})
    picam2.configure(config)
    picam2.start()
    prev_face_detected = False
    voice_proc = None

    while True:
        frame = picam2.capture_array()
        if frame is None:
            break

        detector.setInputSize((frame.shape[1], frame.shape[0]))
        _, faces = detector.detect(frame)
        face_detected = faces is not None and len(faces) > 0

        # Trigger voice loop only once when detection starts (no-face -> face).
        if face_detected and not prev_face_detected:
            if os.path.exists(VOICE_LOOP_SCRIPT):
                if voice_proc is None or voice_proc.poll() is not None:
                    voice_proc = subprocess.Popen([sys.executable, VOICE_LOOP_SCRIPT])
            else:
                print(f"Missing script: {VOICE_LOOP_SCRIPT}")

        prev_face_detected = face_detected

        if faces is not None:
            for face in faces:
                x, y, w, h = [int(v) for v in face[:4]]
                x = max(0, x)
                y = max(0, y)
                w = max(1, w)
                h = max(1, h)

                aligned = recognizer.alignCrop(frame, face)
                query_feature = recognizer.feature(aligned)
                name, score = recognize_name(recognizer, query_feature, known_names, known_features)

                if name != "human":
                    with open(WATCH_FILE, "w", encoding="utf-8") as file:
                        file.write(name + "\n")
                else:
                    cv2.imwrite(f"stranger/unknown_{random.randint(0, 999999)}.jpg", frame)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(
                    frame,
                    f"{name} {score:.2f}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

        cv2.imshow("Face Detection", frame)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    picam2.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
