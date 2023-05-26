import json
from flask import Flask, request, jsonify
from ultralytics import YOLO
import os

from train import Predict, PredictAnnot


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get data from body
    file_data = request.get_data()
    result = Predict(file_data)
    imgs = []
    for img in result:
        imgs.append(img)
    return jsonify(imgs)

@app.route('/uploadAnnot', methods=['POST'])
def upload_annot():
    # Get data from body
    file_data = request.get_data()
    result, metrics = PredictAnnot(file_data)
    return jsonify(result)
    



    


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run()