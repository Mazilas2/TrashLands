import cv2 as cv
import numpy as np
import json
import base64
from ultralytics import YOLO
import statistics

model = YOLO("py/best.pt")

def convertImg(img):
    retval, buffer = cv.imencode('.jpg', img)
    img_str = base64.b64encode(buffer)
    img_str = img_str.decode('utf-8')
    return img_str

def decodeFilepaths(filePaths):
    filePaths = filePaths.decode('utf-8')
    filePaths = json.loads(filePaths)
    filePaths = filePaths['file_paths']
    return filePaths

def calculateMetrics(annots, results):
    yolo_boxes = []
    for result in results:
        boxes = result.boxes.xyxy
        boxes = boxes.tolist()
        yolo_boxes.append(boxes)
    print(yolo_boxes)
    TP = 0
    FP = 0
    FN = 0
    RecallList = []
    PrecisionList = []
    F1List = []
    for i, yolo_box in enumerate(yolo_boxes):
        for j, box in enumerate(yolo_box):
            foundBox = False
            for k, annot in enumerate(annots[i]):
                # If IoU > 0.5, TP
                # If IoU < 0.5, FP
                # If no IoU, FN
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])
                xB2 = int(annot[2])
                xA2 = int(annot[0])
                yB2 = int(annot[3])
                yA2 = int(annot[1])
                # Calculate intersection
                xA_intersect = max(xA, xA2)
                yA_intersect = max(yA, yA2)
                xB_intersect = min(xB, xB2)
                yB_intersect = min(yB, yB2)
                # Calculate area of intersection
                area_intersect = max(0, xB_intersect - xA_intersect + 1) * max(0, yB_intersect - yA_intersect + 1)
                # Calculate area of union
                area_box = (xB - xA + 1) * (yB - yA + 1)
                area_annot = (xB2 - xA2 + 1) * (yB2 - yA2 + 1)
                area_union = area_box + area_annot - area_intersect
                # Calculate IoU
                iou = area_intersect / area_union
                if iou > 0.5:
                    TP += 1
                    foundBox = True
                    break
            if foundBox == False:
                FP += 1
        FN = len(annots[i]) - TP
        if (FN < 0):
            FN = 0
        if (TP > len(annots[i])):
            TP = len(annots[i])
        Precision = TP / (TP + FP)
        Recall = TP / (TP + FN)
        F1 = 2 * (Precision * Recall) / (Precision + Recall)
        RecallList.append(Recall)
        PrecisionList.append(Precision)
        F1List.append(F1)
        #print("TP: ", TP)
        #print("FP: ", FP)
        #print("FN: ", FN)
    Precision = statistics.mean(PrecisionList)
    Recall = statistics.mean(RecallList)
    F1 = statistics.mean(F1List)
    metrics = [Precision, Recall, F1]
    #print(metrics)
    return metrics

def Predict(filePaths):
    filePaths = decodeFilepaths(filePaths)
    images = []
    for filePath in filePaths:
        image = cv.imread(filePath)
        images.append(image)
    results = model(images)
    result = []
    coordsBoxes = []
    for i, img in enumerate(images):
        boxes = results[i].boxes.xyxy
        probs = results[i].boxes.conf
        # Append bounding box coordinates to image
        for j, box in enumerate(boxes):
            coords = box.tolist()
            xB = int(coords[2])
            xA = int(coords[0])
            yB = int(coords[3])
            yA = int(coords[1])
            coordsBoxes.append({filePaths[i]: [xA, yA, xB, yB]})
            cv.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv.putText(img, 
                       str(str(probs[j].tolist())[0:4]), 
                       (xA, yA - 10), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Convert image to base64 string
        result.append(convertImg(img))
    return result, coordsBoxes

def PredictAnnot(filePaths):
    filePaths = decodeFilepaths(filePaths)
    for filePath in filePaths:
        if filePath.endswith('.jpg'):
            # Split file path and get name of file
            filePath = filePath.split('\\')
            filePath = filePath[-1]
            filePath = filePath.replace('.jpg', '.txt')
            filePath2 = filePath
            for filePath2 in filePaths:
                if filePath2.endswith('.txt'):
                    filePath2 = filePath2.split('\\')
                    filePath2 = filePath2[-1]
                    if filePath == filePath2:
                        break
            if filePath != filePath2:
                filePaths.remove(filePath)
    for filePath in filePaths:
        if filePath.endswith('.txt'):
            if filePath.replace('.txt', '.jpg') not in filePaths:
                filePaths.remove(filePath)
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
    results = model(images)
    result = []
    for i, img in enumerate(images):
        boxes = results[i].boxes.xyxy
        probs = results[i].boxes.conf
        for j, box in enumerate(boxes):
            coords = box.tolist()
            xB = int(coords[2])
            xA = int(coords[0])
            yB = int(coords[3])
            yA = int(coords[1])
            cv.rectangle(img, (xA, yA), (xB, yB), (0, 255, 0), 2)
            cv.putText(img, str(str(probs[j].tolist())[0:4]), (xA, yA - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        annot = annots[i]
        for j, box in enumerate(annot):
            x = float(box[0])
            y = float(box[1])
            w = float(box[2])
            h = float(box[3])
            x = x * img.shape[1]
            y = y * img.shape[0]
            w = w * img.shape[1]
            h = h * img.shape[0]
            cv.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 0, 255), 2)
            annots[i][j] = [int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2)]
        result.append(convertImg(img))
    metrics = calculateMetrics(annots, results)
    return result, metrics
