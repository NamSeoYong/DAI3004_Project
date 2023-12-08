import numpy as np
import platform
from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt

import uuid
import json
import time
import cv2
import requests

api_url = "https://fqm1z21tga.apigw.ntruss.com/custom/v1/26812/502fae9a89259a9979de79a6cb112541892e8d48cf5f5da8925b2f0d040994be/general"
secret_ley = "Qm1PVXlRbHFQeUtEUUdQSVNXa1ZlbUhhZGJrdGhMWEY="

path = "asset/images/file_A.png"
files = [('file', open(path, 'rb'))]

#API 요청하기
request_json = {'images': [{'format': 'jpg',
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