from flask import Flask, request, jsonify

from train import Predict, PredictAnnot


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get data from body
    file_data = request.get_data()
    result, coordsBoxes = Predict(file_data)
    imgs = []
    json_result = {
        "result": result,
        "coordsBoxes": coordsBoxes
    }
    return jsonify(json_result)

@app.route('/uploadAnnot', methods=['POST'])
def upload_annot():
    # Get data from body
    file_data = request.get_data()
    result, metrics = PredictAnnot(file_data)
    json_result = {
        "result": result,
        "metrics": metrics
    }
    return jsonify(json_result)
    



    


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run()