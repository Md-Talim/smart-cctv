import datetime
import os

import cv2
import face_recognition
import numpy as np

# 1. Load known faces from folder
known_encs = []
known_names = []

for fname in os.listdir("known_faces"):
    img = face_recognition.load_image_file(f"known_faces/{fname}")
    encs = face_recognition.face_encodings(img)

    if encs:
        known_encs.append(encs[0])
        known_names.append(os.path.splitext(fname)[0])

os.makedirs("captures", exist_ok=True)

print(f"Loaded {len(known_names)} known faces: {known_names}")

# 2. Open laptop webcam (0 = default camera)
cap = cv2.VideoCapture(0)

cv2.namedWindow("AI Smart CCTV — press Q to quit", cv2.WINDOW_NORMAL)

cv2.resizeWindow("AI Smart CCTV — press Q to quit", 1280, 720)

# Track recent alerts to avoid spam
alerted = {}

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # 3. Resize for speed (process at 1/4 size)
    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    # 4. Detect face locations and compute encodings
    locs = face_recognition.face_locations(rgb)
    encs = face_recognition.face_encodings(rgb, locs)

    for (top, right, bottom, left), enc in zip(locs, encs):
        # Scale coordinates back up
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 5. Compare with known faces
        matches = face_recognition.compare_faces(known_encs, enc, tolerance=0.5)

        dists = face_recognition.face_distance(known_encs, enc)

        name = "UNKNOWN"
        color = (0, 0, 220)  # Red for unknown

        if known_encs and np.min(dists) < 0.5:
            idx = np.argmin(dists)
            name = known_names[idx]
            color = (0, 200, 0)  # Green for authorised

        # 6. Draw box + label on frame
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        cv2.rectangle(frame, (left, bottom - 28), (right, bottom), color, cv2.FILLED)

        cv2.putText(
            frame,
            name,
            (left + 6, bottom - 8),
            cv2.FONT_HERSHEY_DUPLEX,
            0.6,
            (255, 255, 255),
            1,
        )

        # 7. Alert for unknown faces
        # Save image + print warning
        if name == "UNKNOWN":
            now = datetime.datetime.now()

            key = f"{left},{top}"
            last = alerted.get(key, datetime.datetime.min)

            # Alert once per 10 seconds
            if (now - last).seconds > 10:
                alerted[key] = now

                ts = now.strftime("%Y%m%d_%H%M%S")

                cv2.imwrite(f"captures/intruder_{ts}.jpg", frame)

                print(f"⚠ ALERT: Unknown face at {now.strftime('%H:%M:%S')}")

    # 8. Show live window
    cv2.imshow("AI Smart CCTV — press Q to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
