import cv2 as cv
import numpy as np
from flask import Flask, request, jsonify
import json
import base64


def train(filePaths):
    filePaths = filePaths.decode('utf-8')
    filePaths = json.loads(filePaths)
    filePaths = filePaths['file_paths']
    images = []
    for filePath in filePaths:
        image = cv.imread(filePath)
        images.append(image)
    # Create matcher
    matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    # Create ORB object
    orb = cv.ORB_create()
    # Create list of keypoints and descriptors for each image
    keypoints = []
    descriptors = []
    for image in images:
        kp, des = orb.detectAndCompute(image, None)
        keypoints.append(kp)
        descriptors.append(des)
    # Create list of matches for each image
    matches = []
    for i in range(len(images)):
        match = matcher.match(descriptors[i], descriptors[i])
        matches.append(match)
    # Create list of good matches for each image
    good_matches = []
    for i in range(len(images)):
        good_match = []
        for match in matches[i]:
            if match.distance < 30:
                good_match.append(match)
        good_matches.append(good_match)
    # Create list of points for each image
    points = []
    for i in range(len(images)):
        point = []
        for match in good_matches[i]:
            point.append(keypoints[i][match.queryIdx].pt)
        points.append(point)
    # Show circles around keypoints
    for i in range(len(images)):
        for point in points[i]:
            # Red circle
            # Smaller size of line
            cv.circle(images[i], (int(point[0]), int(point[1])), 10, (0, 0, 255), 1)
    # Convert images to base64 strings
    result = []
    for img in images:
        retval, buffer = cv.imencode('.jpg', img)
        img_str = base64.b64encode(buffer).decode('utf-8')
        result.append(img_str)
    return result