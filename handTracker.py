import cv2
import mediapipe as mp
class HandDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=0, detection_conf=0.7,
                track_conf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detection_conf = detection_conf
        self.track_conf = track_conf
        self.mp_hands = mp.solutions.hands
        ############
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(self.mode, self.maxHands, self.model_complexity,
                                        self.detection_conf, self.track_conf)
        self.mp_draw = mp.solutions.drawing_utils
    def find_hands(self, img):
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        img.flags.writeable = False
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image)
        ##################33
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img
    def find_position(self, image):
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[0]
            all = []
            for id, lms in enumerate(my_hand.landmark):
                h, w,c = image.shape
                cx, cy = int(lms.x * w), int(lms.y * h)
                all.append((id, cx, cy))
            return all