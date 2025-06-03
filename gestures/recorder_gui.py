import cv2
from recognizer import LandmarkRecognizer
import json
import os

def record_gesture_gui(gesture_type="both"):
    recognizer = LandmarkRecognizer()
    cap = cv2.VideoCapture(0)
    print("Press 's' to save snapshot. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        landmarks = recognizer.detect_landmarks(frame)
        if gesture_type == "hand":
            landmarks = {"left_hand": landmarks["left_hand"], "right_hand": landmarks["right_hand"], "shoulders": landmarks["shoulders"]}
        elif gesture_type == "head":
            landmarks = {"face": landmarks["face"], "shoulders": landmarks["shoulders"]}

        for part, points in landmarks.items():
            for p in points:
                x, y = int(p.x * frame.shape[1]), int(p.y * frame.shape[0])
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        cv2.putText(frame, f"Recording: {gesture_type}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Gesture Recorder", frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            name = input("Enter gesture name: ").strip()
            action = input("Enter action name (e.g., 'open_notepad'): ").strip()

            structured = {
                "gesture_name": name,
                "action_name": action,
                "type": gesture_type,
                "landmarks": {
                    k: [[l.x, l.y, l.z] for l in v] for k, v in landmarks.items()
                }
            }

            save_path = f"gestures/gesture_{name}.json"
            with open(save_path, "w") as f:
                json.dump(structured, f, indent=2)

            print(f"✅ Saved: {save_path}")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
