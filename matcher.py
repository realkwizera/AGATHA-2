import json
import os
import time
import cv2
from gestures.recognizer import GestureRecognizer
from actions.action_mapper import ActionMapper
from utils.config import CONFIG

class GestureMatcher:
    def __init__(self, gesture_folder='gestures', mode='both'):
        self.recognizer = GestureRecognizer(mode)
        self.mapper = ActionMapper()
        self.gesture_folder = gesture_folder
        self.gestures = self.load_gestures()

    def load_gestures(self):
        gestures = []
        for file in os.listdir(self.gesture_folder):
            if file.endswith('.json'):
                with open(os.path.join(self.gesture_folder, file), 'r') as f:
                    gestures.append(json.load(f))
        return gestures

    def compare_landmarks(self, lm1, lm2):
        if len(lm1) != len(lm2):
            return float('inf')
        total = 0
        for a, b in zip(lm1, lm2):
            total += ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2) ** 0.5
        return total / len(lm1)

    def match_gesture(self, current_landmarks):
        for gesture in self.gestures:
            match_score = 0
            found = True
            for part in gesture['landmarks']:
                if part not in current_landmarks:
                    found = False
                    break
                score = self.compare_landmarks(current_landmarks[part], gesture['landmarks'][part])
                match_score += score

            if found and match_score < CONFIG["gesture_match_threshold"]:
                return gesture['action']
        return None

    def detect_cancel(self, landmarks):
        # Cancel gesture: head turned left (based on nose and left ear or pose)
        if 'pose' in landmarks:
            nose = landmarks['pose'][0]
            left_shoulder = landmarks['pose'][11]
            if nose.x < left_shoulder.x:
                return True
        return False

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            landmarks = self.recognizer.detect_landmarks(frame)
            structured = {
                k: [[l.x, l.y, l.z] for l in v] for k, v in landmarks.items()
            }

            action = self.match_gesture(structured)
            if action:
                print(f"Gesture matched: {action}. Starting countdown...")
                cancel = False
                for i in range(CONFIG["countdown_duration"], 0, -1):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    lms = self.recognizer.detect_landmarks(frame)
                    if self.detect_cancel({k: [[l.x, l.y, l.z] for l in v] for k, v in lms.items()}):
                        cancel = True
                        print("❌ Action canceled by turning head left!")
                        break
                    print(f"⏳ {i}...")
                    time.sleep(1)

                if not cancel:
                    print(f"✅ Executing action: {action}")
                    self.mapper.execute_action(action)

            cv2.imshow('Gesture Detection', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
