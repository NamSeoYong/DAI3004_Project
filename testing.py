import cv2
import handTracker as hD
import signal
import sys
from easyocr import Reader
import pygame

#############################################################################################
hand_detector = hD.HandDetector()
# 강제 종료 시그널 핸들러
def signal_handler(sig, frame):
    print("KeyboardInterrupt - Program interrupted")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)
# 강제 종료 시그널 등록
signal.signal(signal.SIGINT, signal_handler)
cap = cv2.VideoCapture(0)  # 웹캠 또는 연결된 카메라를 사용하려면 인덱스 변경.
fps = 30  # 프레임 속도 설정
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_count = 0  # 현재 프레임 번호
##############################################################################################
#TTS 준비 코드

 #TTS 함수 정의
def play_tts(response):
    if response in tts_files:
        tts_files[response].play()
    else:
        print("ERROR")

# pygame mixer 초기화
pygame.mixer.init()

#오디오 파일 로드
tts_files = {
    '오른쪽': pygame.mixer.Sound('RIGHT.mp3'),
    '왼쪽': pygame.mixer.Sound('LEFT.mp3'),
    '위': pygame.mixer.Sound('UP.mp3'),
    '아래': pygame.mixer.Sound('BOTTOM.mp3'),
    '성공': pygame.mixer.Sound('SUCCESS.mp3'),
    '왼쪽 아래': pygame.mixer.Sound('LEFT_BOTTOM.mp3'),
    '왼쪽 위': pygame.mixer.Sound('LEFT_UP.mp3'),
    '오른쪽 아래': pygame.mixer.Sound('RIGHT_BOTTOM.mp3'),
    '오른쪽 위': pygame.mixer.Sound('RIGHT_UP.mp3')
}
#############################################################################################
#서명란 OCR 진행 후, finger point와 좌표 비교하여 TTS 안내하기 위한 준비 코드

# EasyOCR 설정
langs = ['ko', 'en']
reader = Reader(lang_list=langs, gpu=True)

results=[]
target_results = ()

#############################################################################################
#서명란 실시간으로 좌표값 받아와서, finger point와 좌표값 비교 후, TTS 안내

while True:
    success, vid = cap.read()
    if not success:
        print("Failed to read video feed.")
        break
    # vid = cv2.flip(vid, 1)  # 영상 좌우 반전 (필요에 따라 사용)
    vid = hand_detector.find_hands(vid)
    positions = hand_detector.find_position(vid)

    #두번째 손가락만 정의
    index_finger = None
    
    if positions is not None:
        # for id, cx, cy  in positions:  # x, y 좌표 추가
        #     cv2.putText(vid, f"({cx}, {cy})", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1) #실시간 화면에 좌표값 출력
        if len(positions) >= 21:
            index_finger = positions[8][1:]
            
    #프레임 당 더하기 1
    frame_count += 1
    #######################################################################################
    #OCR 후,좌표값 비교
    
    # 텍스트 인식 수행
    if frame_count % 30 == 0:
        results = reader.readtext(vid)
    #서명란 인식
    for (bbox, text, prob) in results:
        if ("(인)" in text) or ("(서명)" in text): #####################경우의 수 넣기##################
            target_results = [(bbox, text, prob)]

    if target_results == None:
        continue

    #서명란 좌표값 정의
    for (bbox, text, prob) in target_results:
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        top_right = tuple(map(int,top_right))
        bottom_left = tuple(map(int,bottom_left))
        
        # 서명란에 빨간색 바운딩 박스 그리기
        cv2.rectangle(vid, top_left, bottom_right, (0, 0, 255), 2)
        # print("인식 성공")

        m, n = (None, None) if index_finger is None else index_finger
        if m is not None and n is not None:
            if frame_count %16==0: #말하기 속도  설정
                if m >= top_right[0] and top_right[1] <= n <= bottom_right[1]:
                    play_tts("오른쪽")
                    # print("오른쪽")
                elif m <= top_left[0] and top_left[1] <= n <= bottom_left[1]:
                    play_tts("왼쪽")
                    # print("왼쪽")
                elif top_left[0] <= m <= top_right[0] and n <= top_left[1]:
                    play_tts("아래")
                    # print("아래")
                elif bottom_left[0] <= m <= bottom_right[0] and n >= bottom_right[1]:
                    play_tts("위")
                    # print("위")
                elif top_left[0] >= m and n<=top_left[1]:
                    play_tts("왼쪽 아래")
                    # print("왼쪽 아래")
                elif bottom_right[0] >= m and bottom_right[1]<=n:
                    play_tts("왼쪽 위")
                    # print("왼쪽 위")
                elif m>=top_right[0] and n<=top_right[1]:
                    play_tts("오른쪽 아래")
                    # print("오른쪽 아래")
                elif bottom_left[0]<=m and bottom_left[1]<=n:
                    play_tts("오른쪽 위")
                    # print("오른쪽 위")
                elif top_left[0] <= m <= top_right[0] and top_left[1] <= n <= bottom_left[1]:
                    play_tts("성공")
                    # print("성공")

    #화면 출력
    cv2.imshow('Signature_Detection', vid)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()