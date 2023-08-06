import requests
import json
import cv2
import base64


def cv2_to_base64(image_path):
    image = cv2.imread(image_path)
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tobytes()).decode('utf8')


def ocr_img(image_path):
    try:
        data = {'images': [cv2_to_base64(image_path)], 'visualization': True}
        headers = {"Content-type": "application/json"}
        url = "http://172.19.1.11:8866/predict/chinese_ocr_db_crnn_server"
        r = requests.post(url=url, headers=headers, data=json.dumps(data))
        # 这里返回的r是一个对象，可通过r.json()["results"]来获取识别
        if r.status_code == 200:
            return r.json()["results"]
        else:
            return "请求异常，请联系管理员"
    except Exception as e:
        return "服务器异常，请联系管理员", e