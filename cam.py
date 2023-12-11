import cv2
import mediapipe as mp


def generate_frames():
    boundingbox_arr = []
    with open('text/boundingbox.txt', 'r') as f:
        boundingbox_arr = parse(f.read())

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)

        # 손 인식
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)

                    # Draw circles only for index finger landmarks (5, 7, 8, 9, 6)
                    if idx == 8:
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                        print(f"Landmark {idx}: ({cx}, {cy})")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def parse(boundingbox_arr):
    tmp = boundingbox_arr.split(";")   
    arr = [int(i) for i in tmp]
    return arr
