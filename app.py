from flask import Flask, render_template, Response, request, jsonify
import time  
import base64
import os
import subprocess
from cam import generate_frames

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/compare')
def compare():
    return render_template("compare.html")

@app.route('/obect')
def object():
    return render_template('object.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload-image', methods=['POST'])
def upload_image():
    # 클라이언트로부터 이미지 데이터를 받습니다.
    image_data = request.json['image']
    
    # base64 문자열에서 순수한 이미지 데이터만 추출합니다.
    image_data = image_data.split(",")[1]

    # 이미지 데이터를 바이트로 디코딩합니다.
    image_bytes = base64.b64decode(image_data)
    
    # 이미지 파일로 저장합니다.
    folder_path = 'static/uploads'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "uploaded_image.jpg")
    with open(file_path, "wb") as file:
        file.write(image_bytes)

    # 성공 메시지를 반환합니다.
    return jsonify({'message': 'Image uploaded successfully'})


@app.route('/run_script')
def run_scripts():
    # 'a.py' 스크립트 실행
    result_a = subprocess.run(['python', 'ocr.py'], stdout=subprocess.PIPE)
    result_a1 = subprocess.run(['python', 'ocr_capture.py'], stdout=subprocess.PIPE)
    #time.sleep(10)
    # 'b.py' 스크립트 실행
    result_b = subprocess.run(['python', 'comparison.py'], stdout=subprocess.PIPE)

    # 결과 반환
    return '', 204

    # result = subprocess.run(['python', 'comparison.py'], stdout=subprocess.PIPE)
    # return jsonify(result=result.stdout.decode('utf-8'))

@app.route('/get_similarity')
def get_similarity():
    try:
        with open('text/result.txt', 'r') as file:
            similarity = file.read().strip()
            return jsonify(similarity=similarity)
    except FileNotFoundError:
        return jsonify(similarity="파일을 찾을 수 없습니다.")

@app.route('/receive_image_choice', methods=['POST'])
def receive_image_choice():
    letter = request.form['letter']
    # letter 값을 사용한 로직
    with open('text/click.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(letter)    
    return '',204

if __name__=='__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
