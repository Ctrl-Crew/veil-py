
from flask import Flask, jsonify, request

from lib import ocr

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get_ocr", methods=["POST"])
def get_ocr():
    data = request.get_json()
    img_data = data.get('img')
    text = ocr.do_ocr(img_data)

    return ocr.post_process(text)