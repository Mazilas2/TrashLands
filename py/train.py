import cv2 as cv
import numpy as np
from flask import Flask, request, jsonify
import json
import base64
from ultralytics import YOLO


def train():
    model = YOLO('yolov8n.pt')
    results = model.train(
        data='Water Trash Dataset/data.yaml',
        imgsz=640,
        epochs=100,
        batch=16,
        name='yolov8n_custom'
    )


def predict():
    model = YOLO('runs/detect/yolov8n_custom0005/weights/best.pt')
    # Confidence Threshold = 5%
    # Overlap Threshold = 20%
    results = model.predict(
        "C:/Datasets/test3.jpg",
        conf=0.05,
        iou=0.2,
        save=True
    )
