import cv2
import numpy as np
import os
import random

# Prepare folder for strangers
os.makedirs("stranger", exist_ok=True)

# Load Haar Cascade for detection
cascade_path = os.path.join(os.getcwd(), "haarcascades", "haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(cascade_path)

# Path to known faces
known_faces_dir = "./images/"
known_names = []
faces_train = []
labels_train = []

label_id = 0
name_map = {}

for filename in os.listdir(known_faces_dir):
    img = cv2.imread(os.path.join(known_faces_dir, filename), cv2.IMREAD_GRAYSCALE)
    faces_train.append(img)
    labels_train.append(label_id)
    name_map[label_id] = filename.split(".")[0]
    label_id += 1
    print(faces_train)
# If you can't use cv2.face.LBPHFaceRecognizer_create() on Pi 5, skip recognition
recognition_available = False
try:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces_train, np.array(labels_train))
    recognition_available = True
except AttributeError:
    print("LBPH recognizer not available on this OpenCV build, using detection only")

# Start camera
cap = cv2.VideoCapture(0)

while True:
 
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]

        if recognition_available and faces_train:
            label, confidence = recognizer.predict(face_img)
            print(confidence)
            if confidence < 100:
                name = name_map[label]
               #speak("Hi, "+name)
                with open("watch.txt", "w", encoding="utf-8") as f:
                    f.write(name + "\n")
            else:
                name = "Unknown"
                cv2.imwrite(f"stranger/unknown_{random.randint(0,999999)}.jpg", frame)
        #else:
         #   name = "Face"
          #  cv2.imwrite(f"stranger/unknown_{random.randint(0,999999)}.jpg", frame)

        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("Face Detection", frame)
    if cv2.waitKey(300) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
