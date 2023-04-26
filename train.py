import cv2 as cv
import numpy as np
import json

# Read image from folder /Water Trash Dataset/images/train
# and convert to grayscale
#

def train(filePaths):
    # Filepath = '../Water Trash Dataset/images/train'
    filePaths = filePaths.decode('utf-8')
    filePaths = json.loads(filePaths)
    filePaths = filePaths['file_paths']
    images = []
    for filePath in filePaths:
        image = cv.imread(filePath)
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
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
            cv.circle(images[i], (int(point[0]), int(point[1])), 10, (0, 255, 0), 2)
    # Show images
    #for i in range(len(images)):
    #    cv.imshow('Image ' + str(i), images[i])
    #cv.waitKey(0)
    # Return list of images with circles around keypoints
    _, buffer = cv.imencode('.png', images)
    return buffer.tobytes()
