import json
from flask import Flask, request, jsonify
import os

from train import train

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get data from body
    file_data = request.get_data()
    result = train(file_data)
    imgs = []
    for img in result:
        imgs.append(img)
    return jsonify(imgs)

    


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run()