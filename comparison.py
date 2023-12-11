import pygame
from difflib import SequenceMatcher
import time

pygame.mixer.init()
# file은 txt파일 넣어야 함
def similar(file_a, file_b):
    with open(file_a, "r", encoding="utf-8") as a:
        A = a.read()
    with open(file_b, "r", encoding="utf-8") as b:
        B = b.read()
        similarity = round(float(SequenceMatcher(None, A, B).ratio()), 2) * 100
        
    with open('text/result.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(str(similarity))    
        
    ten = int(similarity//10)
    one = int(similarity%10)
    print(ten, one)
    num = ['static/tts/0.mp3', 'static/tts/1.mp3','static/tts/2.mp3','static/tts/3.mp3','static/tts/4.mp3','static/tts/5.mp3','static/tts/6.mp3','static/tts/7.mp3','static/tts/8.mp3','static/tts/9.mp3', 'static/tts/10.mp3']
    
    if (ten > 0 ):
        # playsound(num[ten])
        # playsound(num[10])
        
        mySound = pygame.mixer.Sound(num[ten])
        mySound.play()
        time.sleep(0.7)
        mySound.stop()
        mySound = pygame.mixer.Sound(num[10])
        mySound.play()
        time.sleep(0.7)
        mySound.stop()
  
    
    # playsound(num[one])
   
    # playsound('tts/퍼센트.mp3')
    mySound = pygame.mixer.Sound(num[one])
    mySound.play()
    time.sleep(0.7)
    mySound.stop()
  
    mySound = pygame.mixer.Sound('static/tts/퍼센트.mp3')
    mySound.play()
    time.sleep(1)
    mySound.stop()
    
    print(similarity)
    
    
    
    return similarity


cc = ''
with open('text/click.txt', "r", encoding="utf-8") as a:
        cc = a.read()
        
        
if (cc == 'A'):
    similar('text/A.txt', 'text/output.txt')
elif (cc == 'B'):
    similar('text/B.txt', 'text/output.txt')
elif (cc == 'C'):
    similar('text/C.txt', 'text/output.txt')


print("Text saved to: re.txt")
