import mediapipe as mp
import cv2

mp_holistic = mp.solutions.holistic

class GestureRecognizer:
    def __init__(self, mode='both'):
        self.mode = mode  # 'hand', 'head', 'both'
        self.holistic = mp_holistic.Holistic(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            refine_face_landmarks=True
        )

    def detect_landmarks(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.holistic.process(rgb_frame)

        landmarks = {}

        if self.mode in ['head', 'both']:
            if result.face_landmarks:
                landmarks['face'] = result.face_landmarks.landmark
            if result.pose_landmarks:
                landmarks['pose'] = result.pose_landmarks.landmark

        if self.mode in ['hand', 'both']:
            if result.left_hand_landmarks:
                landmarks['left_hand'] = result.left_hand_landmarks.landmark
            if result.right_hand_landmarks:
                landmarks['right_hand'] = result.right_hand_landmarks.landmark

        return landmarks
