# DAI3004_Project

## Team Members

- 팀장 : 남서용 (컴퓨터학부, 한양대학교 ERICA)
- 팀원 : 김다영 (인공지능학과, 한양대학교 ERICA)
- 팀원 : 김은채 (인공지능학과, 한양대학교 ERICA)
- 팀원 : 임은지 (인공지능학과, 한양대학교 ERICA)

## Introduction

이 프로젝트는 시각장애인 이용자를 위한 이미지 인식을 통해 일상생활의 불편을 덜어주는 것을 목적으로 하여, 서명란의 위치가 어디에 있는지 안내 및 오프라인 종이로 나오는 서류의 내용을 기존에 자신이 서명하려 했던 서류가 맞는지 유사율을 나타낸다.

## Contents

0. [Folder Structure](#folder-structure)
1. [Deelopment Setting](#development-setting)
2. [Libraries & Tools](#libraries--tools)
3. [Pages]
4. [서류 비교]
5. [서명란 인식]
6. [Demo](#demo)

### Folder Structure

```
DAI3004_Project
├── LICENSE
├── README.md
├── app.py
├── cam.py
├── comparison.py
├── ocr.py
├── ocr_capture.py
├── src
├── static
│   ├── favicon.ico
│   ├── file.jpg
│   ├── images
│   │   ├── file_A.png
│   │   ├── file_B.png
│   │   └── file_C.png
│   ├── script.js
│   ├── style.css
│   ├── tts
│   └── uploads
├── templates
│   ├── compare.html
│   ├── index.html
│   └── object.html
├── text
│   ├── A.txt
│   ├── B.txt
│   ├── C.txt
│   ├── boundingbox.txt
│   ├── click.txt
│   ├── output.txt
│   └── result.txt
├── tmp.md
└── tts
```

### Development Setting

- Ubuntu 20.04
- Python 3.8
- etc...

### Libraries & Tools

- easyocr
- Flask
- matplotlib
- mediapipe
- numpy
- opencv-python
- Pillow
- pygame
- PyYAML
- requests
- scipy
- sounddevice
- etc...

### Pages

### Demo

1. requirements를 설치한다.

```
pip install -r requirements.txt
```

2. 메인 디렉토리 내의 app.py를 실행한다.

```
python app.py
```

3. 본인이 설정한 포트로 접속한다. Ex) 'http://127.0.0.1:443'
