
from matplotlib import pyplot as plt
import uuid
import json
import time
import cv2
import requests


def plt_imshow(title='image', img=None, figsize=(8, 5)):
    plt.figure(figsize=figsize)
    
    if type(img) == list:
        if type(title) == list:
            titles = title
        else:
            titles = []

            for i in range(len(img)):
                titles.append(title)

        for i in range(len(img)):
            if len(img[i].shape) <= 2:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_GRAY2RGB)
            else:
                rgbImg = cv2.cvtColor(img[i], cv2.COLOR_BGR2RGB)

            plt.subplot(1, len(img), i + 1)
            plt.imshow(rgbImg)
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])

        plt.show()
    else:
        if len(img.shape) < 3:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(rgbImg)
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()



cc = ''

with open('text/click.txt', "r", encoding="utf-8") as a:
        cc = a.read()



new_image_path = ''
files = []

if (cc == 'A'):
    new_image_path = 'static/images/picture_A.jpg'
    files = [('file', open(new_image_path,'rb'))]
    
elif (cc == 'B'):
    new_image_path = 'static/images/picture_B.jpg'
    files = [('file', open(new_image_path,'rb'))]
    
elif (cc == 'C'):
    new_image_path = 'static/images/picture_C.jpg'
    files = [('file', open(new_image_path,'rb'))]
    
print("클릭: ", cc)
print("new_image_path: ", new_image_path)

print("files: ", files)

import cv2

# 이미지 읽기 시도
img = cv2.imread(new_image_path)

if img is not None:
    print("이미지를 성공적으로 읽었습니다.")
else:
    print("이미지를 읽는 데 문제가 발생했습니다.")

api_url = "https://e6tqb8wkgp.apigw.ntruss.com/custom/v1/26841/d7f55303bdf438981aad17e4984a06521341e5ace1745fa94b459d554db93e6c/general"
secret_key = "eml4VEFRQmZTaFBHZklqY0pzS1FlVGdJWlJKWFlsa3I="



#API 요청하기
request_json = {'images': [{'format': 'PNG',
                                'name': 'demo'
                               }],
                    'requestId': str(uuid.uuid4()),
                    'version': 'V2',
                    'timestamp': int(round(time.time() * 1000))
                   }
 
payload = {'message': json.dumps(request_json).encode('UTF-8')}
 
headers = {
  'X-OCR-SECRET': secret_key,
}
 
response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
result = response.json()


img = cv2.imread(new_image_path)
roi_img = img.copy()

text=""
result_text=""
cnt=0
boundingbox=""

for field in result['images'][0]['fields']:
    text = field['inferText']
    result_text+= text
    vertices_list = field['boundingPoly']['vertices']
    cnt+=1
    print(f"cnt : {cnt}")
    print(f"vertices_list : {vertices_list}")
    pts = [tuple(vertice.values()) for vertice in vertices_list]
    print(f"pts : {pts}")
    print('\n')
    topLeft = [int(_) for _ in pts[0]]
    topRight = [int(_) for _ in pts[1]]
    bottomRight = [int(_) for _ in pts[2]]
    bottomLeft = [int(_) for _ in pts[3]]
    
    #초록색 바운딩 박스 그리기
    cv2.line(roi_img, topLeft, topRight, (0,255,0), 2)
    cv2.line(roi_img, topRight, bottomRight, (0,255,0), 2)
    cv2.line(roi_img, bottomRight, bottomLeft, (0,255,0), 2)
    cv2.line(roi_img, bottomLeft, topLeft, (0,255,0), 2)
    #roi_img = put_text(roi_img, text, topLeft[0], topLeft[1] - 10, font_size=30)

    #서명 부분 빨간색으로 바운딩 박스 그리기
    if text == "(인)":
        print(f"Bounding Box Coordinates for '(인)': TopLeft={topLeft}, TopRight={topRight}, BottomRight={bottomRight}, BottomLeft={bottomLeft}")
        boundingbox = f"{topLeft[0]};{topLeft[1]};{topRight[0]};{topRight[1]};{bottomLeft[0]};{bottomLeft[1]};{topRight[0]};{topRight[1]}"
        target_topLeft, target_topRight, target_bottomRight, target_bottomLeft = topLeft, topRight, bottomRight, bottomLeft

        #빨간색 바운딩 박스 그리기
        cv2.line(roi_img, target_topLeft, target_topRight, (0,0,255), 2)
        cv2.line(roi_img, target_topRight, target_bottomRight, (0,0,255), 2)
        cv2.line(roi_img, target_bottomRight, target_bottomLeft, (0,0,255), 2)
        cv2.line(roi_img, target_bottomLeft, target_topLeft, (0,0,255), 2)

    if "서명" in text:
        print(f"Bounding Box Coordinates for '(인)': TopLeft={topLeft}, TopRight={topRight}, BottomRight={bottomRight}, BottomLeft={bottomLeft}")
        boundingbox = f"{topLeft[0]};{topLeft[1]};{topRight[0]};{topRight[1]};{bottomLeft[0]};{bottomLeft[1]};{topRight[0]};{topRight[1]}"
        target_topLeft, target_topRight, target_bottomRight, target_bottomLeft = topLeft, topRight, bottomRight, bottomLeft

        #빨간색 바운딩 박스 그리기
        cv2.line(roi_img, target_topLeft, target_topRight, (0,0,255), 2)
        cv2.line(roi_img, target_topRight, target_bottomRight, (0,0,255), 2)
        cv2.line(roi_img, target_bottomRight, target_bottomLeft, (0,0,255), 2)
        cv2.line(roi_img, target_bottomLeft, target_topLeft, (0,0,255), 2)

print(result_text)
# plt_imshow(["Original", "ROI"], [img, roi_img], figsize=(16, 10))

with open('text/output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(result_text)
with open('text/boundingbox.txt', 'w', encoding='utf-8') as file:
    file.write(boundingbox)

print("Text saved to: output.txt")



