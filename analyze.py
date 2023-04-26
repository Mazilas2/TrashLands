import cv2 as cv
import numpy as np

# Read keypoints.npy, descriptors.npy, and matches.npy
keypoints = np.load('keypoints.npy')
descriptors = np.load('descriptors.npy')
matches = np.load('matches.npy')

# Create a Brute Force Matcher object
