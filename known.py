import os

import face_recognition

known_dir = "known_faces"

for f in os.listdir(known_dir):
    img = face_recognition.load_image_file(f"{known_dir}/{f}")
    encs = face_recognition.face_encodings(img)
    if encs:
        print(f"✓ Loaded: {f}")
    else:
        print(f"✗ No face found in: {f}")
