import cv2
import mediapipe as mp
import time
import pygame

def generate_frames():
    pygame.init()
    cnt = 0
    boundingbox_arr = []
    with open('text/boundingbox.txt', 'r') as f:
        boundingbox_arr = parse(f.read())
    pt1 = (boundingbox_arr[0], boundingbox_arr[1])
    pt2 = (boundingbox_arr[2], boundingbox_arr[3])
    pt3 = (boundingbox_arr[4], boundingbox_arr[5])
    pt4 = (boundingbox_arr[6], boundingbox_arr[7])

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, frame = cap.read()
        if not success:
            break
        # frame = cv2.flip(frame, 1)
        cv2.line(frame, pt1, pt2, (0, 0, 255), 2) # 상
        cv2.line(frame, pt2, pt3, (0, 0, 255), 2) # 우
        cv2.line(frame, pt3, pt4, (0, 0, 255), 2) # 하
        cv2.line(frame, pt4, pt1, (0, 0, 255), 2) # 좌
        # 손 인식
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)

                    if idx == 8:
                        cnt += 1
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                        position = check_position(cx, cy, pt1, pt2, pt3, pt4)
                        print(f"x: {cx}, y: {cy}, 위치: {position}")
                        if cnt % 30 == 0:
                            tts(position)
        print(cnt)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        
    cap.release()
    pygame.quit()

def parse(boundingbox_arr):
    tmp = boundingbox_arr.split(";")   
    arr = [int(i) for i in tmp]
    return arr

def check_position(cx, cy, pt1, pt2, pt3, pt4):
    # 바운딩 박스의 x, y 범위 계산
    left = min(pt1[0], pt2[0], pt3[0], pt4[0])
    right = max(pt1[0], pt2[0], pt3[0], pt4[0])
    top = min(pt1[1], pt2[1], pt3[1], pt4[1])
    bottom = max(pt1[1], pt2[1], pt3[1], pt4[1])

    if left <= cx <= right and top <= cy <= bottom:
        return '확인'
    elif cx < left:
        return '좌'
    elif cx > right:
        return '우'
    elif cy < top:
        return '상'
    elif cy > bottom:
        return '하' 
    
def tts(position):
    if position == '확인':
        sound = pygame.mixer.Sound("tts/SUCCESS.mp3")
        sound.play()
        time.sleep(0.1)
    elif position == '좌':
        sound = pygame.mixer.Sound("tts/LEFT.mp3")
        sound.play()
        time.sleep(0.1)
    elif position == '우':
        sound = pygame.mixer.Sound("tts/RIGHT.mp3")
        sound.play()
        time.sleep(0.1)
    elif position == '상':
        sound = pygame.mixer.Sound("tts/UP.mp3")
        sound.play()
        time.sleep(0.1)
    elif position == '하':
        sound = pygame.mixer.Sound("tts/DOWN.mp3")
        sound.play()
        time.sleep(0.1)