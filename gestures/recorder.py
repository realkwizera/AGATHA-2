import json
from uuid import uuid4
from gestures.recognizer import GestureRecognizer

class GestureRecorder:
    def __init__(self, mode='both'):
        self.recognizer = GestureRecognizer(mode)

    def record(self, frame, action_name):
        landmarks = self.recognizer.detect_landmarks(frame)
        if not landmarks:
            return False

        data = {
            'action': action_name,
            'landmarks': {
                k: [[l.x, l.y, l.z] for l in v] for k, v in landmarks.items()
            }
        }

        filename = f"gesture_{action_name}_{uuid4().hex[:8]}.json"
        with open(f"gestures/{filename}", 'w') as f:
            json.dump(data, f, indent=2)

        return filename
