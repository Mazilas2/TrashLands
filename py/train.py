import cv2 as cv
import numpy as np
from flask import Flask, request, jsonify
import json
import base64
from PIL import Image
from ultralytics import YOLO

model = YOLO("py/best.pt")

def Predict(filePaths):
    filePaths = filePaths.decode('utf-8')
    filePaths = json.loads(filePaths)
    filePaths = filePaths['file_paths']
    images = []
    for filePath in filePaths:
        image = cv.imread(filePath)
        images.append(image)
    # Predict
    results = model(images)
    # Convert images to base64 strings
    # Set result images to images
    result = []
    for i, img in enumerate(images):
        boxes = results[i].boxes.xyxy
        probs = results[i].boxes.conf
        # Append bounding box coordinates to image
        for i, box in enumerate(boxes):
            coords = box.tolist()
            xB = int(coords[2])
            xA = int(coords[0])
            yB = int(coords[3])
            yA = int(coords[1])
            cv.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv.putText(img, str(str(probs[i].tolist())[0:4]), (xA, yA - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Convert image to base64 string
        retval, buffer = cv.imencode('.jpg', img)
        img_str = base64.b64encode(buffer)
        img_str = img_str.decode('utf-8')
        result.append(img_str)
    return result

def PredictAnnot(filePaths):
    filePaths = filePaths.decode('utf-8')
    filePaths = json.loads(filePaths)
    filePaths = filePaths['file_paths']
    images = []
    annots = []
    for filePath in filePaths:
        if filePath.endswith('.txt'):
            with open(filePath, 'r') as f:
                # Remove \n from each line
                annot = f.readlines()
                annot = [x.strip() for x in annot]
                annot = [x.split(' ') for x in annot]
                annot = [x[1:5] for x in annot]
                annot = [[float(y) for y in x] for x in annot]
                annots.append(annot)
        elif filePath.endswith('.jpg'):
            image = cv.imread(filePath)
            images.append(image)
    # Predict
    results = model(images)
    result = []
    for i, img in enumerate(images):
        boxes = results[i].boxes.xyxy
        probs = results[i].boxes.conf
        # Append bounding box coordinates to image
        for i, box in enumerate(boxes):
            coords = box.tolist()
            xB = int(coords[2])
            xA = int(coords[0])
            yB = int(coords[3])
            yA = int(coords[1])
            cv.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv.putText(img, str(str(probs[i].tolist())[0:4]), (xA, yA - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        for i, annot in enumerate(annots):
            for j, box in enumerate(annot):
                x = float(box[0])
                y = float(box[1])
                w = float(box[2])
                h = float(box[3])
                #x = int(x * img.shape[1])
                #y = int(y * img.shape[0])
                #w = int(w * img.shape[1])
                #h = int(h * img.shape[0])
                print(x, y, w, h)
                cv.rectangle(img, (int(x*img.shape[1]), int(y*img.shape[0])), (int((x+w)*img.shape[1]), int((y+h)*img.shape[0])), (0, 0, 255), 2)
        # Convert image to base64 string
        retval, buffer = cv.imencode('.jpg', img)
        img_str = base64.b64encode(buffer)
        img_str = img_str.decode('utf-8')
        result.append(img_str)
    return result
