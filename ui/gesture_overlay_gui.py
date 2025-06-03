import cv2
import time
from matcher import GestureMatcher
from action_mapper import ActionMapper

class GestureOverlayApp:
    def __init__(self):
        self.matcher = GestureMatcher()
        self.cap = cv2.VideoCapture(0)
        self.action_mapper = ActionMapper()
        self.last_match = None
        self.countdown_start = None
        self.countdown_duration = 5  # seconds

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue

            result = self.matcher.process_frame(frame)

            if result["match"]:
                gesture_name = result["gesture_name"]
                action_name = result["action_name"]

                if self.last_match != gesture_name:
                    self.countdown_start = time.time()
                    self.last_match = gesture_name

                elapsed = time.time() - self.countdown_start
                remaining = int(self.countdown_duration - elapsed)

                # Display matched gesture and countdown
                overlay = f"Matched: {gesture_name} -> {action_name} | Executing in: {remaining}s"
                cv2.putText(frame, overlay, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

                # Cancel logic (turn head left)
                if result["cancel"]:
                    cv2.putText(frame, "🚫 Action Canceled!", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    self.last_match = None
                    self.countdown_start = None
                elif elapsed >= self.countdown_duration:
                    self.action_mapper.perform_action(action_name)
                    self.last_match = None
                    self.countdown_start = None
            else:
                cv2.putText(frame, "No match", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (100, 100, 100), 2)
                self.last_match = None
                self.countdown_start = None

            cv2.imshow("🧠 Gesture Overlay Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
